import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import altair as alt

# ==========================================
# 設定エリア
# ==========================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1cPSPPkZLCwvC3O6uQDu1mT86f9Qwqx34Vspml7lPAVo/edit?gid=0#gid=0"

POKEMON_LIST = [
    "ガブリアス","エルフーン","イダイトウ♂","ヤバソチャ","ガオガエン","ドドゲザン","リザードン","オオニューラ","ムクホーク","ニンフィア","ペリッパー","ブリジュラス","リキキリン","ラグラージ","ライチュウ","メタグロス","オーロンゲ","プテラ","サーフゴー","ヤミラミ","コータス","フラエッテ(えいえん)","クチート","フシギバナ","カイリュー","イッカネズミ","バンギラス","ユキメノコ","ミロカロス","ウォッシュロトム","サザンドラ","キュウコン(アローラ)","コノヨザル","ファイアロー","マフォクシー","ガルーラ","ゲンガー","バシャーモ","アシレーヌ","カエンジシ","ジュカイン","バクフーン(ヒスイ)","カメックス","ニョロトノ","サーナイト","シビルドン","ズルズキン","キラフロル","マスカーニャ","ヒートロトム","ドリュウズ","アーマーガア","ヤレユータン","アマージョ","エルレイド","ハッサム","スコヴィラン","ソウブレイズ","ゾロアーク(ヒスイ)","メガニウム","ピクシー","マンムー","ドラミドロ","ブリムオン","イダイトウ♀","ドラパルト","バクーダ","ビビヨン","ミミッキュ","ドヒドイデ","ギャラドス","ウインディ(ヒスイ)","キュウコン","ギルガルド(シールド)","ギルガルド(ブレード)","ジャラランガ","ジジーロン","ラフレシア","ウルガモス","スターミー","バイバニラ","ゲッコウガ","カラマネロ","グレンアルマ","マニューラ","マリルリ","カビゴン","ニャオニクス♂","ルカリオ","ルガルガン(たそがれ)","ダイケンキ(ヒスイ)","ハリーマン","シャンデラ","デカヌチャン","ゴルーグ","オニシズクモ","ケケンカニ","ウインディ","ユキノオー","バサギリ","ボスゴドラ","ミミロップ","クエスパトラ","ハガネール","エレザード","ヤドキング(ガラル)","ラウドボーン","ハラバリー","イルカマン(ナイーブ)","イルカマン(マイティ)","ジャローダ","ルチャブル","ハカドッグ","サンダース","デンリュウ","エンペルト","ヌメルゴン(ヒスイ)","クレッフィ","ローブシン","ドサイドン","グライオン","バンバドロ","メタモン","ランクルス","アヤシシ","ミカルゲ","フロストロトム","ブラッキー","デスカーン","ジュナイパー(ヒスイ)","ペンドラー","バリコオル","オーダイル","フーディン","グレイシア","チルタリス","ケンタロス(パルデア水)","カットロトム","エアームド","ヤドラン","カミツオロチ","ワルビアル","ミミズズ","ヤドラン(ガラル)","オンバーン","カイリキー","レパルダス","ブリガロン","ブロスター","ゴウカザル","カバルドン","デスバーン","マホイップ","タイレーツ","アマルルガ","ライボルト","オニゴーリ","バクフーン","ヘラクロス","ガメノデス","フレフワン","ヤドキング","タブンネ","チャーレム","エンニュート","シャワーズ","ドダイトス","ジュペッタ","ドクロッグ","ムシャーナ","ケンタロス(パルデア炎)","エーフィ","キョジオーン","チリーン","ピカチュウ","ルガルガン(まひる)","ウツボット","オーロット","ウェーニバル","ラムパルド","サメハダー","ヘルガー","ツンベアー","カイロス","リーフィア","クレベース(ヒスイ)","ヌメルゴン","ニャオニクス♀","モルペコ","エンブオー","ドデカバシ","ロズレイド","レントラー","ピジョット","ガチゴラス","ゴロンダ","フラージェス","スピアー","ホルード","ライチュウ(アローラ)","アリアドス","アブソル","ゾロアーク","エモンガ","ポットデス","サダイジャ","タルップル","マッギョ","パンプジン(特大)","ジュナイパー","ロトム","アップリュー","クレベース","スピンロトム","ナゲツケサル","トリデプス","ブースター","フォレトス","ハリーセン","ルガルガン(まよなか)","トリミアン","デデンネ","ケンタロス","ヒヤッキー","アーボック","ペロリーム","ポワルン","ケンタロス(パルデア単)","ダストダス","パンプジン(普通)","ダイケンキ","マッギョ(ガラル)","パンプジン(小)","パンプジン(大)","ヤナッキー","バオッキー","ミルホッグ"
]

# 自分の固定パーティ6匹
MY_PARTY = [
    "イダイトウ♂","エルフーン","ムクホーク","サーフゴー","ヒートロトム","アシレーヌ"
]

# カタカナをひらがなに変換するルール
kata2hira = str.maketrans(
    "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴ", 
    "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんゔ"
)
display_to_orig = {f"{p} ({p.translate(kata2hira)})": p for p in POKEMON_LIST}

# ==========================================
# スプレッドシート連携
# ==========================================
@st.cache_resource
def init_connection():
    key_dict = json.loads(st.secrets["gcp_service_account"]["key"])
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(key_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_url(SHEET_URL).sheet1

sheet = init_connection()

def load_data():
    records = sheet.get_all_records()
    return pd.DataFrame(records)

# ==========================================
# データ保存処理（バグ回避のための裏側処理）
# ==========================================
if "reset_counter" not in st.session_state:
    st.session_state.reset_counter = 0

def save_record():
    rk = st.session_state.reset_counter
    
    # 画面の入力内容を取得
    selected_display = st.session_state.get(f"opp_6_widget_{rk}", [])
    current_opp_6 = [display_to_orig[s] for s in selected_display]
    
    opp_lead = st.session_state.get(f"opp_lead_{rk}", [])
    opp_back = st.session_state.get(f"opp_back_{rk}", [])
    my_lead = st.session_state.get(f"my_lead_{rk}", [])
    my_back = st.session_state.get(f"my_back_{rk}", [])
    result = st.session_state.get(f"result_widget_{rk}")

    # エラーチェック
    if len(current_opp_6) == 0:
        st.session_state.msg = ("error", "相手のパーティを1匹以上選んでください。")
        return
    if len(opp_lead) != 2 or len(opp_back) != 2:
        st.session_state.msg = ("error", "相手の先発と後発を2匹ずつ選んでください。")
        return
    if set(opp_lead) & set(opp_back):
        st.session_state.msg = ("error", "相手の先発と後発で同じポケモンが選ばれています。")
        return
    if len(my_lead) != 2 or len(my_back) != 2:
        st.session_state.msg = ("error", "自分の先発と後発を2匹ずつ選んでください。")
        return
    if set(my_lead) & set(my_back):
        st.session_state.msg = ("error", "自分の先発と後発で同じポケモンが選ばれています。")
        return
    if result is None:
        st.session_state.msg = ("error", "勝敗を選択してください。")
        return

    # 保存データの整形
    opp_6_str = ", ".join(current_opp_6)
    opp_4_str = ", ".join(opp_lead + opp_back)
    opp_lead_str = ", ".join(opp_lead)
    my_4_str = ", ".join(my_lead + my_back)
    my_lead_str = ", ".join(my_lead)
    current_party_str = ", ".join(sorted(MY_PARTY))
    date_str = pd.Timestamp.now("Asia/Tokyo").strftime("%Y-%m-%d %H:%M")
    
    # スプレッドシートに追記 (順番: 日時, 相手6, 相手選出, 自分選出, 勝敗, 自分先発, 相手先発, 自分6)
    sheet.append_row([date_str, opp_6_str, opp_4_str, my_4_str, result, my_lead_str, opp_lead_str, current_party_str])
    
    # 成功メッセージと画面のリセット
    st.session_state.msg = ("success", "記録を保存しました！")
    st.session_state.reset_counter += 1

# ==========================================
# メイン画面：対戦記録
# ==========================================
st.title("ポケモンチャンピオンズ 対戦記録")

# メッセージ表示用
if "msg" in st.session_state:
    msg_type, msg_text = st.session_state.msg
    if msg_type == "error":
        st.error(msg_text)
    else:
        st.success(msg_text)
    del st.session_state.msg

rk = st.session_state.reset_counter

st.header("新しい対戦の記録")

# --- ① 相手のパーティを入力 ---
selected_display = st.multiselect(
    "▼ 相手のパーティ6匹を選択", 
    options=list(display_to_orig.keys()),
    max_selections=6,
    key=f"opp_6_widget_{rk}",
    placeholder="検索..."
)
current_opp_6 = [display_to_orig[s] for s in selected_display]

st.write("---")

# --- ② 選出と結果を記録 ---
with st.form("form_record"):
    st.write("▼ 選出と先発を記録")
    
    # 【追加機能】順番を気にせず「先発」と「後発」を分けて選択させることで正確にデータを取ります
    st.write("**【相手の選出】**")
    opp_lead = st.pills("相手の先発 (2匹)", options=current_opp_6, selection_mode="multi", key=f"opp_lead_{rk}")
    opp_back = st.pills("相手の後発 (2匹)", options=current_opp_6, selection_mode="multi", key=f"opp_back_{rk}")
    
    st.write("**【自分の選出】**")
    my_lead = st.pills("自分の先発 (2匹)", options=MY_PARTY, selection_mode="multi", key=f"my_lead_{rk}")
    my_back = st.pills("自分の後発 (2匹)", options=MY_PARTY, selection_mode="multi", key=f"my_back_{rk}")
    
    st.write("---")
    result = st.radio("勝敗", ["勝ち", "負け"], horizontal=True, index=None, key=f"result_widget_{rk}")
    
    # ボタンを押した時に「save_record」を裏側で実行させる
    st.form_submit_button("スプレッドシートに保存", on_click=save_record)

# ==========================================
# 分析画面：選出率と履歴
# ==========================================
st.header("データ分析")
df = load_data()

if not df.empty:
# --- パーティごとの絞り込み ---
    if "自分の6匹" in df.columns:
        def sort_party_str(party_str):
            if pd.isna(party_str) or str(party_str).strip() == "": return ""
            return ", ".join(sorted([p.strip() for p in str(party_str).split(",") if p.strip()]))
        
        df["分析用パーティ"] = df["自分の6匹"].apply(sort_party_str)
        party_history = [p for p in df["分析用パーティ"].unique() if p != ""]
        current_party_str = ", ".join(sorted(MY_PARTY))
        if current_party_str not in party_history:
            party_history.insert(0, current_party_str)

        # スマホで見切れないよう、選択肢の文字を省略する関数
        def shorten_party_name(party_str):
            pokemons = [p.strip() for p in party_str.split(",") if p.strip()]
            if len(pokemons) > 3:
                # 最初の3匹だけを表示し、残りは省略する
                return f"{pokemons[0]} / {pokemons[1]} / {pokemons[2]} ... (他{len(pokemons)-3}匹)"
            return party_str

        selected_party = st.selectbox(
            "▼ 分析するパーティを選択", 
            party_history, 
            index=party_history.index(current_party_str) if current_party_str in party_history else 0,
            format_func=shorten_party_name # ← ここで省略関数を適用
        )

        # 選択中のパーティの全員の名前を、枠の下に小さく表示して確認できるようにする
        st.caption(f"【選択中の6匹】 {selected_party}")

        df_filtered = df[df["分析用パーティ"] == selected_party]
    if not df_filtered.empty:
        # --- 勝率表示 ---
        win_count = len(df_filtered[df_filtered["勝敗"] == "勝ち"])
        total_count = len(df_filtered)
        st.write(f"**総対戦数:** {total_count} 戦 / **勝ち:** {win_count} 勝 / **勝率:** {(win_count/total_count)*100:.1f} %")
        st.write("---")

        # --- 相手の選出率・先発率の分析 ---
        if "相手の6匹" in df.columns and "相手の選出" in df.columns:
            st.subheader("相手のポケモンの選出率・先発率")
            
            # スマホからタップしやすい並び替えボタン
            sort_target = st.radio(
                "並び替え", 
                ["遭遇回数 が多い順", "選出率 が高い順", "先発率 が高い順"], 
                horizontal=True
            )
            
            opp_data = []
            for idx, row in df_filtered.iterrows():
                opp_6_str = str(row.get("相手の6匹", ""))
                opp_4_str = str(row.get("相手の選出", ""))
                opp_lead_str = str(row.get("相手の先発", ""))
                
                # 先発データがちゃんと記録されている試合かどうかを判定
                has_lead_data = pd.notna(opp_lead_str) and opp_lead_str.strip() != ""
                
                if pd.notna(opp_6_str) and opp_6_str.strip() != "":
                    o_6 = [p.strip() for p in opp_6_str.split(",") if p.strip()]
                    o_4 = [p.strip() for p in opp_4_str.split(",") if p.strip()] if pd.notna(opp_4_str) else []
                    o_lead = [p.strip() for p in opp_lead_str.split(",") if p.strip()] if has_lead_data else []
                    
                    for p in o_6:
                        opp_data.append({
                            "ポケモン": p,
                            "選出": 1 if p in o_4 else 0,
                            "先発": 1 if p in o_lead else 0,
                            "先発有効対戦": 1 if has_lead_data else 0 # 過去の空欄データを無視するためのフラグ
                        })
            
            if opp_data:
                opp_df = pd.DataFrame(opp_data)
                
                # ポケモンごとに集計
                stats_df = opp_df.groupby("ポケモン").agg(
                    遭遇回数=("ポケモン", "count"),
                    選出回数=("選出", "sum"),
                    先発回数=("先発", "sum"),
                    先発有効対戦数=("先発有効対戦", "sum")
                ).reset_index()
                
                # 確率の計算（先発率は、先発データがある試合だけを分母にする）
                stats_df["選出率"] = (stats_df["選出回数"] / stats_df["遭遇回数"]) * 100
                
                # ゼロ除算エラーを防ぐため、先発有効対戦数が0の時は先発率も0にする
                stats_df["先発率"] = stats_df.apply(
                    lambda x: (x["先発回数"] / x["先発有効対戦数"] * 100) if x["先発有効対戦数"] > 0 else 0.0, 
                    axis=1
                )
                
                # ラジオボタンの選択に合わせて並び替えを実行
                if "遭遇回数" in sort_target:
                    stats_df = stats_df.sort_values(by=["遭遇回数", "選出率"], ascending=[False, False])
                elif "選出率" in sort_target:
                    stats_df = stats_df.sort_values(by=["選出率", "遭遇回数"], ascending=[False, False])
                elif "先発率" in sort_target:
                    stats_df = stats_df.sort_values(by=["先発率", "遭遇回数"], ascending=[False, False])
                
                # 表示用のデータフレームを整理
                display_df = stats_df[["ポケモン", "遭遇回数", "選出率", "先発率"]].copy()
                display_df["選出率"] = display_df["選出率"].apply(lambda x: f"{x:.1f}%")
                display_df["先発率"] = display_df["先発率"].apply(lambda x: f"{x:.1f}%")
                
                # スマホでもスッキリ見やすい表として出力（hide_indexで左端の数字を消す）
                st.dataframe(display_df, use_container_width=True, hide_index=True)
            else:
                st.info("集計できる相手のデータがありません。")
            
            st.write("---")

        # --- 自分の選出割合 ---
        st.subheader("自分のポケモンの選出回数")
        all_my_picks = []
        for picks in df_filtered["自分の選出"]:
            all_my_picks.extend([p.strip() for p in str(picks).split(",") if p.strip()])
        
        if all_my_picks:
            pick_counts = pd.Series(all_my_picks).value_counts().reset_index()
            pick_counts.columns = ['ポケモン', '選出回数']
            chart = alt.Chart(pick_counts).mark_bar().encode(
                x=alt.X('ポケモン', sort=None, title='ポケモン'),
                y=alt.Y('選出回数', title='選出回数'),
                tooltip=['ポケモン', '選出回数']
            )
            st.altair_chart(chart, use_container_width=True)

        st.subheader("直近の対戦履歴")
        # 履歴もインデックスを隠してスッキリさせる
        st.dataframe(df_filtered.sort_index(ascending=False).head(20), hide_index=True)
    else:
        st.info("このパーティでの対戦記録はまだありません。")
else:
    st.info("まだスプレッドシートにデータがありません。")