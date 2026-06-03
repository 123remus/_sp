# 程式實作說明

## 概述

本作業實作了三個經典的執行緒同步問題，全部使用 C 語言 + POSIX Threads（pthread）。

所有程式都使用 **Mutex（互斥鎖）** 來保護共享資源，並在哲學家用餐問題中展示了如何透過**統一的鎖定順序**來避免 Deadlock。

---

## 1. 銀行存提款模擬 (`bank.c`)

### 問題描述

同一個銀行帳戶，一個執行緒存款 100000 次，另一個執行緒提款 100000 次。如果沒有同步機制，Race Condition 會導致最終餘額不正確。

### 解決方案

使用 `pthread_mutex_t` 保護 `balance` 變數。每次存/提款前鎖定 Mutex，操作完成後解鎖：

```c
pthread_mutex_lock(&mutex);
balance++;
pthread_mutex_unlock(&mutex);
```

### 正確性驗證

預期最終餘額為 `0`（存款 100000 次 +1，提款 100000 次 -1）。

如果不使用 Mutex，由於 Race Condition，最終餘額幾乎永遠不會是 0。

### 執行結果範例

```
Final balance: 0 (expected: 0)
Test PASSED
```

---

## 2. 生產者消費者問題 (`prodcon.c`)

### 問題描述

多個生產者執行緒生產資料放入有界緩衝區（Bounded Buffer），多個消費者執行緒從緩衝區取出資料。需要解決：
- 緩衝區滿時生產者必須等待
- 緩衝區空時消費者必須等待
- 多個生產者/消費者不能同時存取緩衝區

### 解決方案

使用三種同步工具：

| 工具 | 用途 |
|------|------|
| `pthread_mutex_t` | 保護緩衝區的互斥存取 |
| `pthread_cond_t`（cond_producer） | 緩衝區滿時讓生產者等待 |
| `pthread_cond_t`（cond_consumer） | 緩衝區空時讓消費者等待 |

### 流程

```
生產者:
  1. 鎖定 Mutex
  2. 如果緩衝區已滿，等待 cond_producer
  3. 放入資料
  4. 喚醒 cond_consumer
  5. 解鎖 Mutex

消費者:
  1. 鎖定 Mutex
  2. 如果緩衝區為空，等待 cond_consumer
  3. 取出資料
  4. 喚醒 cond_producer
  5. 解鎖 Mutex
```

### 注意事項

- 使用 `while` 迴圈檢查條件（而非 `if`），避免 Spurious Wakeup（虛假的喚醒）
- 先解鎖再喚醒，或喚醒後立即解鎖，以減少上下文切換開銷

---

## 3. 哲學家用餐問題 (`dining.c`)

### 問題描述

五位哲學家坐在圓桌前，每人左右各有一根筷子。哲學家要吃飯必須同時取得兩根筷子。如果所有哲學家同時拿起左邊的筷子，就會發生 **Deadlock**——所有人都在等右邊的筷子。

### 解決方案

破壞「循環等待」條件：規定統一的資源取得順序，每位哲學家**先拿編號較小的筷子**。

```c
int left = id;
int right = (id + 1) % N;

if (left < right) {
    // 先拿左（編號小），再拿右（編號大）
    pthread_mutex_lock(&chopsticks[left]);
    pthread_mutex_lock(&chopsticks[right]);
} else {
    // 先拿右（編號小），再拿左（編號大）
    pthread_mutex_lock(&chopsticks[right]);
    pthread_mutex_lock(&chopsticks[left]);
}
```

### 為什麼這樣可以避免 Deadlock

當所有哲學家都依照編號順序拿筷子時，最後一位哲學家（編號最大）無法同時拿到較小和較大的筷子，因為較小的筷子可能被別人拿著，但這保證了**至少有一位哲學家可以拿到兩根筷子**，打破了循環等待。

### 追蹤範例（5 位哲學家）

```
哲學家 0：先拿 0，再拿 1   (編號小→大)
哲學家 1：先拿 1，再拿 2
哲學家 2：先拿 2，再拿 3
哲學家 3：先拿 3，再拿 4
哲學家 4：先拿 0（因為 0 < 4），再拿 4  ← 0 被哲學家 0 拿著，所以哲學家 4 等待
```

哲學家 4 被擋住了，但哲學家 0~3 可以順利進行，不會形成完整的循環等待鏈。

---

## 編譯與執行

```bash
# 編譯所有程式
gcc -pthread bank.c -o bank
gcc -pthread prodcon.c -o prodcon
gcc -pthread dining.c -o dining

# 執行
./bank
./prodcon
./dining
```

## 總結

| 程式 | 使用的同步機制 | 主要展示 |
|------|---------------|----------|
| `bank.c` | Mutex | Race Condition 解決、臨界區段保護 |
| `prodcon.c` | Mutex + Condition Variable | 有界緩衝區、生產者消費者模式 |
| `dining.c` | Mutex + 統一的鎖定順序 | Deadlock 預防（破壞循環等待） |
