import streamlit as st
import pandas as pd
import os

# 保存するCSVファイル名
DB_FILE = "pokemon_battle_logs.csv"

st.title("⚔️ ポケモン チャンピオンズ 対戦記録")

# データの読み込み
def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    else:
        return pd.DataFrame(columns=[
            "日付", "相手の6匹", "相手の選出", "自分の選出", "勝敗", "最後の生存"
        ])

df = load_data()

# 入力フォーム
st.header("📝 新しい対戦の記録")
with st.form("battle_form", clear_on_submit=True):
    opp_6 = st.text_input("相手のパーティ6匹")
    opp_4 = st.text_input("相手の選出4匹")
    my_4 = st.text_input("自分の選出4匹")
    result = st.radio("勝敗", ["勝ち", "負け"], horizontal=True)
    last_pokemon = st.text_input("最後に場に残ったポケモン")
    submit_button = st.form_submit_button("記録する")

# 保存処理
if submit_button:
    if opp_6 and opp_4 and my_4:
        new_data = pd.DataFrame([{
            "日付": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
            "相手の6匹": opp_6, "相手の選出": opp_4, "自分の選出": my_4,
            "勝敗": result, "最後の生存": last_pokemon
        }])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success("保存しました！")
    else:
        st.error("パーティと選出は入力必須です。")

# 履歴表示
st.header("📊 対戦履歴")
if not df.empty:
    st.dataframe(df.sort_index(ascending=False))
else:
    st.info("まだ対戦記録がありません。")