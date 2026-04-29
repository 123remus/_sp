# VoxLang EBNF 語法規範

## 1. 詞法規則

```
letter     = "A" | "B" | ... | "Z" | "a" | "b" | ... | "z"
digit      = "0" | "1" | ... | "9"
ident      = letter { letter | digit }
intLiteral = ["-"] digit { digit }
floatLiteral = ["-"] digit { digit } "." digit { digit }
stringLiteral = '"' { all characters except '"' } '"'
booleanLiteral = "true" | "false"
```

## 2. 保留關鍵字

```
var, func, if, else, while, for, break, continue, return,
int, float, bool, string, array, void
```

## 3. 運算子

```
+   -   *   /   %
==  !=  <   >   <=  >=
&&  ||  !
=   :   ->  ,   (   )   [   ]   {   }
```

## 4. 語法規則 (EBNF)

### 4.1 程式結構

```
Program          = { Statement } ;

Statement        = VariableDecl
                  | FunctionDecl
                  | IfStatement
                  | WhileStatement
                  | ForStatement
                  | BreakStatement
                  | ContinueStatement
                  | ReturnStatement
                  | ExpressionStatement
                  | Block ;

Block            = "{" { Statement } "}" ;
```

### 4.2 變數和函式

```
VariableDecl     = "var" Ident ":" Type "=" Expression ";" ;

FunctionDecl     = "func" Ident "(" [ ParameterList ] ")" "->" Type Block ;

ParameterList     = Parameter { "," Parameter } ;
Parameter        = Ident ":" Type ;

Type             = "int" | "float" | "bool" | "string" | "array" | "void" ;
```

### 4.3 控制流

```
IfStatement      = "if" "(" Expression ")" Block [ "else" Block ] ;

WhileStatement   = "while" "(" Expression ")" Block ;

ForStatement     = "for" "(" VariableDecl ";" Expression ";" Expression ")" Block ;

BreakStatement   = "break" ";" ;
ContinueStatement = "continue" ";" ;
ReturnStatement  = "return" [ Expression ] ";" ;
```

### 4.4 表達式

```
Expression       = AssignmentExpr ;

AssignmentExpr   = LogicalOrExpr [ "=" Expression ] ;

LogicalOrExpr    = LogicalAndExpr { "||" LogicalAndExpr } ;

LogicalAndExpr   = EqualityExpr { "&&" EqualityExpr } ;

EqualityExpr      = RelationalExpr { ("==" | "!=") RelationalExpr } ;

RelationalExpr    = AdditiveExpr { ("<" | ">" | "<=" | ">=") AdditiveExpr } ;

AdditiveExpr      = MultiplicativeExpr { ("+" | "-") MultiplicativeExpr } ;

MultiplicativeExpr = UnaryExpr { ("*" | "/" | "%") UnaryExpr } ;

UnaryExpr         = ("+" | "-" | "!") UnaryExpr
                  | CallExpr ;

CallExpr          = PrimaryExpr [ "(" [ ArgumentList ] ")" ]
                  | PrimaryExpr "[" Expression "]" ;

ArgumentList      = Expression { "," Expression } ;

PrimaryExpr       = Ident
                  | Literal
                  | "(" Expression ")" ;

Literal           = intLiteral
                  | floatLiteral
                  | stringLiteral
                  | booleanLiteral
                  | ArrayLiteral ;

ArrayLiteral      = "[" [ Expression { "," Expression } ] "]" ;
```

## 5. 範例解析

```
// 原始碼
var x: int = 10;
func add(a: int, b: int) -> int {
    return a + b;
}

// 語法樹
Program
├── VariableDecl (x: int = 10)
└── FunctionDecl (add, params: [a:int, b:int], ret: int)
    └── Block
        └── ReturnStatement (a + b)
```