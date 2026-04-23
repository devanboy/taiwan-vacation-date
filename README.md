# taiwan-vacation-date 🇹🇼

一個超簡單的 Python 工具，幫你找出**利用台灣連假（國定假日）出國旅遊**的最佳日期組合，並且自動計算每一組日期你需要**請幾天假**。

> 💡 **核心概念**：把連假往前後延伸幾天，湊出 4~7 天的短天數出國行程，同時讓你請的假最少、CP 值最高。

---

## ✨ 功能亮點

| 功能 | 說明 |
|------|------|
| 📅 **自動抓取國定假日** | 從 [TaiwanCalendar](https://github.com/ruyut/TaiwanCalendar) 即時取得最新行事曆，無需手動維護 |
| 🧮 **自動計算請假天數** | 逐日檢查每段行程中「真正需要請假的上班日」有幾天 |
| 🔀 **多條件篩選** | 可自訂搜尋區間、最大延長天數、行程長度範圍 |
| 🚫 **自動去重** | 同一組出發/回程只會出現一次 |

---

## 📦 安裝

```bash
pip install taiwan-vacation-date
```

或者直接把 `taiwan_vacation_date.py` 放在你的專案裡使用。

---

## 🚀 快速開始

### 基本用法

```python
from taiwan_vacation_date import taiwan_vacation_date

# 預設：搜尋未來 365 天，最多請 4 天假，行程 4~7 天
results = taiwan_vacation_date()

for dep, ret, leave in results:
    print(f"出發: {dep}  回程: {ret}  需請假: {leave} 天")
```

### 輸出範例

```
出發: 2026-04-28  回程: 2026-05-04  需請假: 1 天
出發: 2026-04-29  回程: 2026-05-04  需請假: 0 天
出發: 2026-05-01  回程: 2026-05-05  需請假: 0 天
出發: 2026-09-24  回程: 2026-09-28  需請假: 2 天
```

> 🎯 **數字越小表示越划算**——0 天請假代表全程都在連假 & 週末！

---

## ⚙️ 參數說明

```python
taiwan_vacation_date(
    duration=365,        # 搜尋天數：從今天起往後找幾天
    extension_day=4,     # 最多可請假天數（前後延伸合計）
    min_total_days=4,    # 最短行程天數
    max_total_days=7,    # 最長行程天數
)
```

| 參數 | 類型 | 預設 | 說明 |
|------|------|------|------|
| `duration` | `int` | `365` | 搜尋區間（天）。例如 `180` 代表只看未來半年 |
| `extension_day` | `int` | `4` | 願意請的假天數上限。例如 `2` 代表只請 2 天假 |
| `min_total_days` | `int` | `4` | 行程最少幾天 |
| `max_total_days` | `int` | `7` | 行程最多幾天 |

### 不同場景範例

#### 🏃 只想請 1~2 天假、湊 4 天出國
```python
results = taiwan_vacation_date(
    duration=180,
    extension_day=2,
    min_total_days=4,
    max_total_days=5,
)
```

#### ✈️ 國慶雙十長假大膽請 4 天，湊出 9~10 天
```python
results = taiwan_vacation_date(
    duration=365,
    extension_day=4,
    min_total_days=9,
    max_total_days=10,
)
```

---

## 📊 回傳格式

回傳一個 **Nx3 二維陣列**（list of lists）：

```python
[
    ["2026-02-14", "2026-02-22", 2],   # 出發, 回程, 需請假天數
    ["2026-04-28", "2026-05-04", 1],
    ["2026-05-01", "2026-05-05", 0],
    ...
]
```

| 索引 | 內容 | 範例 |
|------|------|------|
| `[0]` | 出發日期 | `"2026-02-14"` |
| `[1]` | 回程日期 | `"2026-02-22"` |
| `[2]` | 需請假天數 | `2` |

---

## 📡 資料來源

行事曆資料來自開源專案 [ruyut/TaiwanCalendar](https://github.com/ruyut/TaiwanCalendar)，透過 **jsDelivr CDN** 即時下載，確保資料永遠是最新的。

---

## 🧪 直接執行測試

```bash
python taiwan_vacation_date.py
```

會自動印出未來一年所有最划算的連假出國組合！

---

## 📁 專案結構

```
taiwan-vacation-date/
├── taiwan_vacation_date.py   # 主要函式
├── __init__.py               # 模組入口
├── README.md                 # 說明文件 (本檔)
└── LICENSE                   # MIT License
```

---

## 🤝 貢獻

歡迎 Fork / PR / Issue！如果你發現行事曆資料有誤或想新增功能，請直接開 Issue。

---

## 📜 License

MIT License — 自由使用、修改、散佈。

---

Made with ❤️ in Taiwan
