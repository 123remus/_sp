# HW7：微型 Shell（命令列直譯器）與多行程管理

## 專案概述

本專案實作一個名為 **mysh** 的微型 Shell，展示 Unix 行程管理（process management）的核心概念，包括：

- 命令列解析與執行
- 行程建立（`fork`）
- 外部程式載入（`execvp`）
- 行程同步（`waitpid`）
- 背景執行（`&`）
- 訊號處理（`SIGCHLD`）
- I/O 重導向（`>` / `<`）
- 管道（`|`）

## 功能列表

| 功能         | 說明                              |
| ------------ | --------------------------------- |
| `cd [dir]`   | 切換工作目錄                      |
| `pwd`        | 顯示目前目錄                      |
| `exit`       | 離開 Shell                        |
| `jobs`       | 列出背景工作                      |
| `help`       | 顯示內建指令說明                  |
| `<command> &` | 背景執行                         |
| `cmd1 \| cmd2` | 管道串接                       |
| `cmd > file` | 輸出重導向                        |
| `cmd < file` | 輸入重導向                        |

## 編譯與執行

```bash
make          # 編譯
make run      # 編譯並執行
./mysh        # 直接執行
make clean    # 清除編譯產物
```

## 多行程管理機制

1. **行程建立**：透過 `fork()` 建立子行程，子行程以 `execvp()` 載入外部程式。
2. **前景/背景**：前景行程以 `waitpid()` 等待完成；背景行程（結尾加 `&`）不等待，並記錄 PID。
3. **殭屍行程預防**：註冊 `SIGCHLD` 訊號處理器，以 `WNOHANG` 非同步回收已結束的背景子行程。
4. **I/O 重導向**：子行程中以 `dup2()` 將 stdin/stdout 導向至檔案。
5. **管道**：建立 `pipe()`，兩個子行程分別關閉讀/寫端，以 `dup2()` 串接。

## 程式架構

```
mysh.c
├── sigchld_handler()      -- 背景行程回收
├── setup_signal_handlers()-- 註冊訊號處理
├── tokenize()             -- 命令列切詞（支援雙引號）
├── handle_builtin()       -- 處理內建指令
├── has_pipe()             -- 偵測管道運算子
├── execute_piped()        -- 執行管道命令
├── has_redirect()         -- 偵測重導向運算子
├── execute()              -- 統一分派（內建/管道/重導向/一般）
├── shell_loop()           -- 主迴圈（讀取-解析-執行）
└── main()                 -- 進入點
```

## 範例操作

```
mysh:/home/user$ pwd
/home/user
mysh:/home/user$ ls -l
...
mysh:/home/user$ sleep 5 &
[1] 12345
mysh:/home/user$ jobs
[1] 12345
mysh:/home/user$ echo hello > test.txt
mysh:/home/user$ cat < test.txt
hello
mysh:/home/user$ ls | wc -l
...
mysh:/home/user$ help
...
mysh:/home/user$ exit
```

## 環境需求

- Linux / WSL / macOS
- GCC 編譯器
- GNU Make
