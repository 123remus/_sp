# HW5：執行緒同步經典問題

## 內容

| 檔案 | 說明 |
|------|------|
| `threading_concepts.md` | 執行緒、Race Condition、Mutex、Deadlock 觀念說明 |
| `bank.c` | 銀行存提款模擬 — 同帳戶 100000 次存提，用 Mutex 確保正確 |
| `prodcon.c` | 生產者消費者問題模擬 — Bounded Buffer + Mutex + Condition Variable |
| `dining.c` | 哲學家用餐問題模擬 — 5 位哲學家用 Mutex 避免 Deadlock |
| `docs.md` | 上述程式的實作說明 |

## 編譯方式

```bash
# 安裝 pthread (通常已內建)
# Linux:
gcc -pthread bank.c -o bank && ./bank
gcc -pthread prodcon.c -o prodcon && ./prodcon
gcc -pthread dining.c -o dining && ./dining
```
