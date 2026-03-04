## [加入while的AI](https://gemini.google.com/share/a0196b10a62b)
   [遇到困難問的AI](https://gemini.google.com/share/2c4437a7f3a4)

## 2. `while` 處理程式碼之設計原理

實作 `while` 迴圈的設計核心在於**「回跳機制」**與**「回填技術 (Backpatching)」**。

### A. 關鍵步驟解析

1. **保存入口點 (start_pc)**：
在解析 `while` 條件之前，必須先記住目前的指令地址（`quad_count`）。這是因為當迴圈內容執行完畢後，程式必須跳回這裡重新判斷條件是否成立。
2. **條件跳轉 (JMP_F)**：
解析 `while (expression)` 後，生成一個 `JMP_F`（Jump if False）指令。此時我們還不知道迴圈主體（Block）有多長，因此跳轉目標暫時填入 `?`。
3. **無條件回跳 (JMP)**：
在迴圈主體的最後一條指令之後，發出一個無條件跳轉 `JMP`，目標指向第一步保存的 `start_pc`。
4. **回填出口 (Backpatching)**：
一旦主體解析完成，我們就知道「迴圈外面」的地址在哪裡（即目前的 `quad_count`）。此時將第 2 步產生的 `JMP_F` 指令的結果欄位修改為目前的地址。

### B. VM 指令集擴充

為了支援迴圈，VM 必須處理兩種跳轉：

* **JMP_F (條件跳轉)**：用於「當條件不成立時，跳過迴圈主體」。
* **JMP (無條件跳轉)**：用於「執行完主體後，強制回到條件判斷處」。

### C. 執行邏輯圖示

生成的 Quadruples 結構如下：

```text
PC    Op         Arg1    Result
-------------------------------
10    (Condition Logic...)       <-- start_pc
12    JMP_F      t1      16      (若 t1 為 0，跳到結束)
13    (Statement Body...)
15    JMP        -       10      (跳回起點重新判斷)
16    (Next Code...)             <-- 迴圈結束後的目標

```

這樣的設計讓 P0 編譯器能夠處理重複執行的邏輯，且支援巢狀（Nested）結構，因為遞迴下降會利用系統堆疊自動管理不同層級的標籤與地址。

---

