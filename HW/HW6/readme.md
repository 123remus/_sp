# HW6 — Process & File I/O Demo

## 系統呼叫一覽

| System Call | 用途 |
|---|---|
| `fork()` | 建立子行程 |
| `execvp()` | 取代行程映像，執行外部指令 |
| `open()` | 開啟檔案 |
| `close()` | 關閉檔案描述符 |
| `read()` / `write()` | 讀寫資料 |
| `dup2()` | 複製檔案描述符（重導向） |
| `stdin(0)` / `stdout(1)` / `stderr(2)` | 標準輸入／輸出／錯誤 |

## 程式說明

`process_io_demo.c` 接受以下引數：

```
./process_io_demo <input_file> <output_file> <cmd> [args...]
```

1. 用 `open()` 開啟輸入檔（唯讀）與輸出檔（寫入）。
2. 用 `fork()` 建立子行程。
3. 子行程用 `dup2()` 將 stdin/stdout 重導向至上述檔案，再用 `execvp()` 執行指定指令。
4. 父行程用 `waitpid()` 等待子行程結束，並用 `write()` 印出結束狀態。

## 編譯與執行

```bash
gcc -o process_io_demo process_io_demo.c

echo "Hello World" > input.txt
./process_io_demo input.txt output.txt wc -w

cat output.txt  # 應輸出 2
```
