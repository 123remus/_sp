# VoxLang 程式語言

## 專案概述

VoxLang 是一個教學用途的程式語言，採用編譯器架構設計，將原始碼編譯為自訂位元組碼（Bytecode），再由虛擬機器（VM）執行。

## 專案架構

```
HW2/
├── lexer.py          # 詞法分析器 (Lexer)
├── voxast.py         # 語法分析器 (Parser) - 生成抽象語法樹
├── codegen.py        # 位元組碼生成器
├── vm.py             # 虛擬機器 (Virtual Machine)
├── run.py            # 編譯執行腳本
├── docs/
│   ├── LANGUAGE_SPEC.md  # 語言規範
│   └── GRAMMAR.md        # EBNF 語法
└── examples/
    ├── basic.vox         # 基礎測試
    ├── simple.vox       # 簡單測試
    ├── hello.vox        # Hello World + 變數 + 函式
    ├── fibonacci.vox    # 費波那契遞迴
    ├── array_test.vox   # 陣列測試
    └── for_loop.vox    # for 迴圈測試
```

## 語言特性

| 特性 | 說明 |
|------|------|
| **類型系統** | 強類型 (int, float, bool, string, array) |
| **實作方式** | 編譯到位元組碼 + 虛擬機器執行 |
| **目標碼** | 基於堆疊的位元組碼 |
| **函式** | 支援參數和回傳值 |
| **控制流** | if-else, while, for, break, continue |
| **運算子** | 算術 (+,-,*,/,%)，邏輯 (==,!=,<,>,<=,>=,&&,\|\|,!) |

## 使用方式

```bash
# 執行範例檔案
python3 run.py examples/basic.vox
python3 run.py examples/simple.vox
python3 run.py examples/hello.vox
```

## 編譯器架構

1. **詞法分析器 (Lexer)**：將原始碼轉換為 Token 流
2. **語法分析器 (Parser)**：將 Token 流解析為抽象語法樹 (AST)
3. **語意分析**：類型檢查、作用域分析
4. **位元組碼生成器**：將 AST 轉換為位元組碼
5. **虛擬機器 (VM)**：解釋執行位元組碼

## 語法範例

```vox
// 變數宣告
var x: int = 10;
var name: string = "Vox";

// 函式定義
func add(a: int, b: int) -> int {
    return a + b;
}

// 條件判斷
if (x > 5) {
    print("x 大於 5");
} else {
    print("x 小於等於 5");
}

// 迴圈
var i: int = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}
```

## 技術細節

- **實作語言**：Python 3
- **位元組碼設計**：基於堆疊的指令集
- **記憶體管理**：簡單的堆疊式 VM，無垃圾回收機制
- **資料類型**：整數、浮點數、布林值、字串、陣列

## 測試狀態

- 基本變數宣告與輸出：✓ 正常運作
- 函式定義與呼叫：✓ 正常運作
- 運算式與運算子：✓ 正常運作
- if-else 條件判斷：部分正常
- while/for 迴圈：需要修復

## 授權

本專案僅供教學用途。