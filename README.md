# GPA Calc FastAPI

CSV をアップロードして **① 累計 GPA** と **② P/F 評価ではない科目における A 以上（A, A+）の単位割合** を計算するシンプルな Web アプリです。  
フロント（`index.html`）から CSV を送信すると、FastAPI バックエンド（`app.py`）が `calc_gpa.py` のロジックで集計して JSON を返します。

## 特徴
- **FastAPI + pandas** で高速・シンプル
- **CSV を投げるだけ**で GPA と A 以上割合を取得
- A+ のスケール、P/F 判定値、GPA 対象外区分などを **簡単にカスタマイズ**可能

---

## ディレクトリ構成
```
.
├─ app.py          # FastAPI: POST /api/calc（CSVを受け取り計算）
├─ calc_gpa.py     # 集計ロジック（pandas）
└─ index.html      # 簡易フロント（CSVを選んで送信して結果表示）
```

---

## 必要要件
- Python 3.10+（3.11 推奨）
- 主要パッケージ
  ```bash
  pip install fastapi uvicorn pandas python-multipart
  ```

---

## 使い方（クイックスタート）

1. ルートに `app.py`, `calc_gpa.py`, `index.html` を置く。
2. バックエンド起動：
   ```bash
   uvicorn app:app --reload
   ```
   起動後、`http://127.0.0.1:8000/health` で `{"ok": true}` が返ればOK。

3. API を試す（Swagger UI）：
   - `http://127.0.0.1:8000/docs` → **POST /api/calc** → `Try it out` → CSV を選択 → `Execute`  
   - 正常時のレスポンス例：
     ```json
     { "gpa": 3.877, "ratio": 0.8022 }
     ```

4. フロントから使う：
   - `index.html` をブラウザで開く → CSV を選択 → 送信  
   - うまくいかない場合は簡易サーバで配信してもOK：
     ```bash
     python -m http.server 5500
     # → http://127.0.0.1:5500/index.html
     ```

---

## API 仕様

### POST `/api/calc`
- **Content-Type**: `multipart/form-data`
- **Body**: `file`（CSVファイル）
- **Response (200)**:
  ```json
  { "gpa": <float|null>, "ratio": <float|null> }
  ```
  - `gpa` … 小数第3位へ丸めた累計GPA（null は計算不可）
  - `ratio` … A 以上割合（0.0〜1.0、例: 0.8022 は 80.22%）

---

## CSV フォーマット
- **必須列**: `単位数`, `総合評価`  
- **任意列**: `科目区分`（GPA 計算対象外の判定に使用）  
- 列名の前後の空白は自動で除去して解釈します。

---

## 計算ルール（既定）

### ① 累計 GPA
- **GPA 計算対象外科目**を除外
- **P/F 評価ではない**行のみ対象
- 文字評価のみ（`A+`, `A`, `B`, `C`, `D` …）
- 換算は **4.3 制**（`A+`=4.3, `A`=4.0, `B`=3.0, `C`=2.0, `D`=1.0）

### ② A 以上の単位割合
- **P/F 評価ではない**文字評価の総単位を分母
- `A+`/`A` の総単位を分子  
- GPA 対象外科目は **含める**（「P/F 以外」であれば分母に入る）

---

## カスタマイズ
`calc_gpa.py` 冒頭の定数やマップを編集：

- **P/F 判定値**: `PF_VALUES = {"P", "F", "合格", "不合格"}`
- **GPA 対象外の区分名**: `EXCLUDED_CATEGORY = "GPA計算対象外科目"`
- **GPA 換算（A+ を 4.5 にする等）**:
  ```python
  gp_map = {"A+": 4.3, "A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0}
  # 例: A+ を 4.5 にしたい場合は "A+": 4.5 に変更
  ```

---

## トラブルシューティング
- `python-multipart` が無いと言われる  
  → `pip install python-multipart`
- CSV アップロードで 422  
  → Swagger の `file` フィールドに **必ずファイルを選択**。  
- `ModuleNotFoundError: app`  
  → `uvicorn app:app --reload` 実行時の **作業ディレクトリ** に `app.py` があるか確認。
- 別 Python に入れてしまったかも？  
  → `python -c "import sys; print(sys.executable)"` で使われている Python を確認し、その Python に `pip install`。

---

## ライセンス
MIT（必要に応じて変更してください）

---

## 謝辞
- FastAPI — https://fastapi.tiangolo.com/
- pandas — https://pandas.pydata.org/
- Uvicorn — https://www.uvicorn.org/

