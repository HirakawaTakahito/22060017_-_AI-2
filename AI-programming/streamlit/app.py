import streamlit as st
import requests
import datetime
import pandas as pd

API_URL = "https://training-api-p14p.onrender.com"

st.title("🏋️ トレーニングノートアプリ")

# 履歴取得
try:
    history = requests.get(f"{API_URL}/get_history").json()
except Exception as e:
    st.error(f"APIへの接続に失敗しました: {e}")
    st.stop()

# ユーザー名
username = st.selectbox("ユーザー名", history["usernames"] + ["新規入力"])
if username == "新規入力":
    username = st.text_input("新しいユーザー名")

# 日付
date = st.date_input("日付", datetime.date.today())

# 種目
exercise = st.selectbox("種目名", history["exercises"] + ["新規入力"])
if exercise == "新規入力":
    exercise = st.text_input("新しい種目名")

# セット入力
st.subheader("セット入力")
weight = st.number_input("重量(kg)", min_value=0.0, step=0.5)
reps = st.number_input("レップ数", min_value=0, step=1)

if "sets" not in st.session_state:
    st.session_state["sets"] = []

if st.button("セット追加"):
    if weight > 0 and reps > 0:
        st.session_state["sets"].append({"weight": weight, "reps": reps})
    else:
        st.warning("重量とレップ数を正しく入力してください")

if st.session_state["sets"]:
    st.write("追加されたセット")
    st.table(st.session_state["sets"])

# 記録保存
if st.button("記録を保存"):
    if username and exercise and st.session_state["sets"]:
        payload = {
            "username": username,
            "date": str(date),
            "exercise": exercise,
            "sets": st.session_state["sets"]
        }
        try:
            res = requests.post(f"{API_URL}/add_record", json=payload).json()
            st.success(f"保存完了！総負荷量: {res['total_load']} kg")
            st.session_state["sets"] = []
        except Exception as e:
            st.error(f"保存中にエラーが発生しました: {e}")
    else:
        st.warning("全ての項目を入力してください")

# 過去記録とユーザー別グラフ表示
if st.checkbox("過去記録を表示"):
    try:
        records = requests.get(f"{API_URL}/get_records").json()
    except Exception as e:
        st.error(f"記録取得に失敗しました: {e}")
        st.stop()

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df)

        # ユーザー選択
        st.subheader("ユーザーごとの総負荷量推移")
        user_list = sorted(df["username"].unique())
        selected_user = st.selectbox("ユーザーを選択", user_list)

        # ユーザーでフィルタ
        user_df = df[df["username"] == selected_user]

        # 種目選択
        exercise_list = sorted(user_df["exercise"].unique())
        selected_ex = st.selectbox("種目を選択", exercise_list)

        # 種目でフィルタ
        filtered_df = user_df[user_df["exercise"] == selected_ex].copy()
        filtered_df["date"] = pd.to_datetime(filtered_df["date"])

        # 日付ごとに総負荷量集計
        grouped_df = filtered_df.groupby("date")["total_load"].sum().reset_index()

        # 横軸を日付だけに変換
        grouped_df["date"] = grouped_df["date"].dt.strftime("%Y-%m-%d")

        # グラフ描画
        st.bar_chart(grouped_df.set_index("date")["total_load"])
    else:
        st.info("記録がありません")
