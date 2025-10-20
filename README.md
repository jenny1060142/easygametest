# Maze Game

一個簡單的文字版迷宮遊戲（Python）。本程式在 Windows 下支援即時鍵盤輸入（WASD 與方向鍵），並提供 demo 自動示範模式。

## 功能
- 指定大小 n，生成 n × n 的完美迷宮（perfect maze，任意兩格間僅有一條路徑）。
- 邊界用 `#` 顯示，牆用 `█` 表示，通路為空白。
- 隨機起點 `S` 與終點 `E`（會放在邊界上，且不會放在四個角落）。
- 玩家用 `P` 表示，支援鍵盤 `W/A/S/D` 與方向鍵移動，按 `q` 離開。
- 每次使用者操作（包含嘗試移動到牆或邊界失敗）都會計入步數並顯示於迷宮下方。
- 支援顏色顯示（若已安裝 `colorama` 套件）。

## 快速開始
在 PowerShell（Windows）或一般終端機：

```powershell
python maze_game.py --size 7
```

自動示範（非互動）：

```powershell
python maze_game.py --size 7 --demo
```

參數說明：
- `--size N` 或 `-n N`：設定迷宮大小為 N × N（預設 15，最小 3）。
- `--demo`：以自動路徑示範方式顯示解。

## 鍵位
- w 或 上方向鍵：上
- a 或 左方向鍵：左
- s 或 下方向鍵：下
- d 或 右方向鍵：右
- q：離開遊戲

注意：在非 Windows 或 msvcrt 不可用時，互動模式會回退為 `input()` 讀行（需按 Enter）。

## 安裝建議（可選）
若想要有彩色輸出，建議安裝 `colorama`：

```powershell
pip install colorama
```

安裝後再次執行程式即可看到彩色化的 S/E/P、牆與邊界。

## 顯示說明
- `#`：邊界框
- `█`：牆/障礙
- 空格：可通行路徑
- `S`：起點（邊界）
- `E`：終點（邊界）
- `P`：玩家目前位置

步數會顯示為 `Steps: N`，且會在步數下多印一個空行以避免混淆顯示。

## 範例
```powershell
python maze_game.py --size 7 --demo
```

輸出會類似：

```
# # # # # # #
#       █   #
S   █   █   #
#   █       #
#   █ █ █   #
#   █     P E
# # # # # # #
Steps: 10

```

## 限制與未來改進
- 目前在非 Windows 平臺即時按鍵支援有限（可改用 `pynput` 或 `keyboard` 等套件以支援更多平台）。
- 若想要更漂亮的 full-screen 介面，可改用 `curses`（Unix-like）或 `windows-curses`（Windows）實作。想要我幫你改成 full-screen 的 curses UI 嗎？

---

檔案：`maze_game.py`（遊戲主程式）

## 踩地雷小遊戲（Minesweeper）

玩法與操作：
- 選擇一個 N × N 的格子與炸彈數量，程式會隨機放置炸彈（以 `!` 表示）。
- 未揭露格以 `.` 顯示；揭露後若周圍炸彈數為 0 顯示空白，若為 1..8 顯示該數字。
- 在揭露空白格時，會以上下左右四個方向（不包含對角）遞迴展開相連的空白格，並同時顯示相鄰的數字格。
- 標記功能：在互動模式輸入 `m r c` 可以標記或取消標記該格（以 `x` 顯示），用於提示可能的炸彈位置。
- 揭露格子：輸入 `r c`（row col）會揭露該格；若踩到炸彈遊戲結束；若揭露完所有非炸彈格則勝利，並顯示所有炸彈位置。

指令範例（終端互動版）：
```powershell
python minesweeper.py --size 9 --bombs 10
# 遊戲內指令：
#  r c      -> 揭露座標 (row col)
#  m r c    -> 標記/取消標記
#  q        -> 離開遊戲
```

註：行與列會以數字標示，且輸入時請使用空格分隔 row 與 col，例如 `3 5`。
範例：
- 使用 `m r c` 標記，或使用緊湊格式 `m12` / `m1,2` 表示標記 (row=1, col=2)

## 如何開啟 / 執行遊戲檔案

下面是一些在 Windows PowerShell 下可直接複製使用的指令，適用於本專案中的遊戲檔案。

- 執行迷宮遊戲（Python 互動版）：

```powershell
# 進入專案資料夾後執行
python maze_game.py --size 9

# 或指定 demo 模式
python maze_game.py --size 9 --demo
```

- 執行踩地雷遊戲（Python 互動版）：

```powershell
python minesweeper.py --size 9 --bombs 10
```

- 直接以預設瀏覽器開啟 HTML 檔（不啟動伺服器）：

```powershell
# 從該資料夾執行會使用系統預設應用程式（通常是瀏覽器）開啟
Start-Process "D:\\ML\\maze_app.html"
# 或在目前目錄下
Start-Process "maze_app.html"
```

- 在本機以簡單 HTTP server 服務 HTML（當你想要使用 AJAX 或 fetch 呼叫本機檔案時）：

```powershell
# 在專案根目錄啟動一個簡單的 HTTP 伺服器（Python 3）
python -m http.server 8000

# 然後在瀏覽器開啟
Start-Process "http://localhost:8000/maze_app.html"
```

備註：
- 如果你使用虛擬環境（venv/conda），請先啟動該環境再執行 `python`。例如：

```powershell
# venv 範例
.\\venv\\Scripts\\Activate.ps1
python maze_game.py --size 9
```

- 若要顯示彩色輸出，請先安裝 `colorama`：

```powershell
pip install colorama
```
