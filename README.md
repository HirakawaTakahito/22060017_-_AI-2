# 🏋️ トレーニングノートアプリ

## 📌 アプリ概要
本アプリは、ユーザーが日々のトレーニング記録（種目・重量・レップ数）を入力し、総負荷量（重量 × レップ数の合計）を計算・保存します。過去記録をユーザーごとに種目別でグラフ化して推移を確認できます。

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
- **データ保存**: JSONファイル
- **可視化**: pandas, Streamlit chart API

---

## 🔌 API仕様
### `POST /add_record`
トレーニング記録を追加し、総負荷量を返す。


---

## 2. システム設計図（system_diagram.png）
<p align="left">
  <img width="500" height="300" src="system_diagram.png">
</p>

構成イメージはこんな感じ👇  
- 左：ユーザー（ブラウザ）
- 中：Streamlit（UI処理）
- 右：FastAPI（データ処理＋JSON保存）
- 保存先：`records.json`

---

## 3. コード説明図（code_diagram.png）
<p align="left">
  <img width="500" height="300" src="code_diagram.png">
</p>

- `main.py`（FastAPI）
  - `/add_record` → 記録保存＆総負荷量計算
  - `/get_records` → 全記録取得
  - `/get_history` → 入力履歴取得
- `app.py`（Streamlit）
  - UI入力フォーム
  - セット追加機能
  - 保存ボタン
  - 過去記録表示（ユーザー → 種目 → グラフ）

---

## 改善案
夏休み課題の改善案については [improvement.md](./improvement.md) をご覧ください。


