# HW3 - Todo CLI 待辦事項管理工具

## 專案簡介
使用 Python 開發的命令列待辦事項管理工具，支援新增、完成、刪除、搜尋、篩選與統計功能。

## 技術堆疊
- **Python 3.12+**
- **Click** - 命令列介面框架
- **Rich** - 終端美觀輸出（表格、面板、顏色）
- **Pydantic** - 資料驗證與模型
- **pytest** - 單元測試框架

## 功能特色
- 新增待辦事項並設定優先等級（低/中/高）
- 標記完成、刪除待辦
- 列出待辦（支援顯示全部、依優先等級篩選）
- 關鍵字搜尋
- 統計儀表板
- JSON 檔案持久化儲存
- 12 個單元測試全部通過

## 安裝方式

```bash
cd HW3
pip install -e .
```

## 使用方式

```bash
# 新增待辦
todo add "買菜" -p 2
todo add "完成期末報告" -p 3
todo add "看書"

# 列出待辦（預設顯示未完成）
todo list
todo list -a          # 顯示全部（含已完成）
todo list -p 3        # 僅顯示高優先等級

# 標記完成
todo done 1

# 刪除
todo rm 3

# 搜尋
todo search "報告"

# 統計
todo stats
```

## 執行測試

```bash
pytest tests/ -v
```

## 專案結構
```
HW3/
├── pyproject.toml      # 專案設定與依賴
├── README.md           # 本檔案
├── todo_cli/
│   ├── __init__.py
│   ├── main.py         # CLI 命令列入口
│   ├── models.py       # Todo 資料模型
│   └── storage.py      # JSON 持久化儲存
└── tests/
    └── test_todo.py    # 單元測試
```
