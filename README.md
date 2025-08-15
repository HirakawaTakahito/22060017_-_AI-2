# 🏋️ トレーニングノートアプリ

## 📌 アプリ概要
本アプリは、ユーザーが日々のトレーニング記録（種目・重量・レップ数）を入力し、総負荷量（重量 × レップ数の合計）を計算・保存します。  
過去記録をユーザーごと・種目別にグラフ化し、推移を確認できます。

- **入力項目**  
  - ユーザー名（履歴または新規）
  - 日付
  - 種目（履歴または新規）
  - セット（重量・レップ数）

- **出力**  
  - 保存時に総負荷量を表示
  - 過去記録一覧（テーブル表示）
  - ユーザーごとの種目別総負荷量推移（棒グラフ）

---

## 🛠 使用技術
- **バックエンド**: FastAPI
- **フロントエンド**: Streamlit
- **データ保存**: JSONファイル（`data.json`, `history.json`）
- **可視化**: pandas, Streamlit Chart API

---

## 🔌 API仕様

### `POST /add_record`
トレーニング記録を追加し、総負荷量を返す。

**リクエスト例**
```json
{
  "username": "Sumire",
  "date": "2025-08-12",
  "exercise": "Bench Press",
  "sets": [
    {"weight": 70, "reps": 10},
    {"weight": 70, "reps": 5}
  ]
}
🖥 システム設計図


左：ユーザー（ブラウザ）

中央：Streamlit（UI処理）

右：FastAPI（データ処理＋JSON保存）

保存先：data.json と history.json

📜 コード説明図


main.py（FastAPI）

/add_record → 記録保存＆総負荷量計算

/get_records → 全記録取得

/get_history → 入力履歴取得

app.py（Streamlit）

UI入力フォーム

セット追加機能

保存ボタン

過去記録表示（ユーザー → 種目 → グラフ）

🚀 デプロイ情報
アプリURL（Streamlit Cloud）: https://your-streamlit-app.streamlit.app

API URL（Render）: https://xxxxx.onrender.com

