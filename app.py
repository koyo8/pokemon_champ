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

# ポケモンリスト
POKEMON_LIST = [
    "ガブリアス","メガガブリアス","エルフーン","イダイトウ♂","ヤバソチャ","ガオガエン","ドドゲザン","リザードン","メガリザードンX","メガリザードンY","オオニューラ","ムクホーク","メガムクホーク","ニンフィア","ペリッパー","ブリジュラス","リキキリン","ラグラージ","メガラグラージ","ライチュウ","メガライチュウX","メガライチュウY","メタグロス","メガメタグロス","オーロンゲ","プテラ","メガプテラ","サーフゴー","ヤミラミ","メガヤミラミ","コータス","フラエッテ(えいえん)","メガフラエッテ","クチート","メガクチート","フシギバナ","メガフシギバナ","カイリュー","メガカイリュー","イッカネズミ","バンギラス","メガバンギラス","ユキメノコ","メガユキメノコ","ミロカロス","ウォッシュロトム","サザンドラ","キュウコン(アローラ)","コノヨザル","ファイアロー","マフォクシー","メガマフォクシー","ガルーラ","メガガルーラ","ゲンガー","メガゲンガー","バシャーモ","メガバシャーモ","アシレーヌ","カエンジシ","メガカエンジシ","ジュカイン","メガジュカイン","バクフーン(ヒスイ)","カメックス","メガカメックス","ニョロトノ","サーナイト","メガサーナイト","シビルドン","メガシビルドン","ズルズキン","メガズルズキン","キラフロル","メガキラフロル","マスカーニャ","ヒートロトム","ドリュウズ","メガドリュウズ","アーマーガア","ヤレユータン","アマージョ","エルレイド","メガエルレイド","ハッサム","メガハッサム","スコヴィラン","メガスコヴィラン","ソウブレイズ","ゾロアーク(ヒスイ)","メガニウム","メガメガニウム","ピクシー","メガピクシー","マンムー","ドラミドロ","メガドラミドロ","ブリムオン","イダイトウ♀","ドラパルト","バクーダ","メガバクーダ","ビビヨン","ミミッキュ","ドヒドイデ","ギャラドス","メガギャラドス","ウインディ(ヒスイ)","キュウコン","ギルガルド(シールド)","ギルガルド(ブレード)","ジャラランガ","ジジーロン","メガジジーロン","ラフレシア","ウルガモス","スターミー","メガスターミー","バイバニラ","ゲッコウガ","メガゲッコウガ","カラマネロ","メガカラマネロ","グレンアルマ","マニューラ","マリルリ","カビゴン","ニャオニクス♂","メガニャオニクス♂","ルカリオ","メガルカリオ","ルガルガン(たそがれ)","ダイケンキ(ヒスイ)","ハリーマン","シャンデラ","メガシャンデラ","デカヌチャン","ゴルーグ","メガゴルーグ","オニシズクモ","ケケンカニ","メガケケンカニ","ウインディ","ユキノオー","メガユキノオー","バサギリ","ボスゴドラ","メガボスゴドラ","ミミロップ","メガミミロップ","クエスパトラ","ハガネール","メガハガネール","エレザード","ヤドキング(ガラル)","ラウドボーン","ハラバリー","イルカマン(ナイーブ)","イルカマン(マイティ)","ジャローダ","ルチャブル","メガルチャブル","ハカドッグ","サンダース","デンリュウ","メガデンリュウ","エンペルト","ヌメルゴン(ヒスイ)","クレッフィ","ローブシン","ドサイドン","グライオン","バンバドロ","メタモン","ランクルス","アヤシシ","ミカルゲ","フロストロトム","ブラッキー","デスカーン","ジュナイパー(ヒスイ)","ペンドラー","メガペンドラー","バリコオル","オーダイル","メガオーダイル","フーディン","メガフーディン","グレイシア","チルタリス","メガチルタリス","ケンタロス(パルデア水)","カットロトム","エアームド","メガエアームド","ヤドラン","メガヤドラン","カミツオロチ","ワルビアル","ミミズズ","ヤドラン(ガラル)","オンバーン","カイリキー","レパルダス","ブリガロン","メガブリガロン","ブロスター","ゴウカザル","カバルドン","デスバーン","マホイップ","タイレーツ","メガタイレーツ","アマルルガ","ライボルト","メガライボルト","オニゴーリ","メガオニゴーリ","バクフーン","ヘラクロス","メガヘラクロス","ガメノデス","メガガメノデス","フレフワン","ヤドキング","タブンネ","メガタブンネ","チャーレム","メガチャーレム","エンニュート","シャワーズ","ドダイトス","ジュペッタ","メガジュペッタ","ドクロッグ","ムシャーナ","ケンタロス(パルデア炎)","エーフィ","キョジオーン","チリーン","メガチリーン","ピカチュウ","ルガルガン(まひる)","ウツボット","メガウツボット","オーロット","ウェーニバル","ラムパルド","サメハダー","メガサメハダー","ヘルガー","メガヘルガー","ツンベアー","カイロス","メガカイロス","リーフィア","クレベース(ヒスイ)","ヌメルゴン","ニャオニクス♀","メガニャオニクス♀","モルペコ","エンブオー","メガエンブオー","ドデカバシ","ロズレイド","レントラー","ピジョット","メガピジョット","ガチゴラス","ゴロンダ","フラージェス","スピアー","メガスピアー","ホルード","ライチュウ(アローラ)","アリアドス","アブソル","メガアブソル","ゾロアーク","エモンガ","ポットデス","サダイジャ","タルップル","マッギョ","パンプジン(特大)","ジュナイパー","ロトム","アップリュー","クレベース","スピンロトム","ナゲツケサル","トリデプス","ブースター","フォレトス","ハリーセン","ルガルガン(まよなか)","トリミアン","デデンネ","ケンタロス","ヒヤッキー","アーボック","ペロリーム","ポワルン","ケンタロス(パルデア単)","ダストダス","パンプジン(普通)","ダイケンキ","マッギョ(ガラル)","パンプジン(小)","パンプジン(大)","ヤナッキー","バオッキー","ミルホッグ"
]

# 自分の固定パーティ6匹
MY_PARTY = [
    "イダイトウ♂","エルフーン","メガムクホーク","サーフゴー","ヒートロトム","アシレーヌ"
]

# ==========================================
# スプレッドシート連携の準備
# ==========================================
@st.cache_resource
def init_connection():
    # StreamlitのSecretsから鍵情報を読み込む
    key_dict = json.loads(st.secrets["gcp_service_account"]["key"])
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(key_dict, scopes=scopes)
    client = gspread.authorize(creds)
    return client.open_by_url(SHEET_URL).sheet1

sheet = init_connection()

# データの読み込み
def load_data():
    records = sheet.get_all_records()
    return pd.DataFrame(records)

df = load_data()

# ==========================================
# メイン画面：対戦記録
# ==========================================
st.title("ポケモン チャンピオンズ 対戦記録")

st.header("新しい対戦の記録")

# --- 画面切り替えのための状態管理 ---
if "step" not in st.session_state: st.session_state.step = 1
if "opp_6" not in st.session_state: st.session_state.opp_6 = []

# ==========================================
# ステップ1：相手のパーティ選択
# ==========================================
if st.session_state.step == 1:
    st.subheader("① 相手のパーティ6匹を登録")
    st.info("※ 検索文字を変更すると選択がリセットされるため、検索を使う場合は文字を消さずにまとめて選ぶか、スクロールして探してください。")
    
    # 検索機能
    hira2kata = str.maketrans(
        "ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをん", 
        "ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲン"
    )
    search_word = st.text_input("検索（ひらがなOK）", "")
    
    if search_word:
        kata_search = search_word.translate(hira2kata)
        filtered_options = [p for p in POKEMON_LIST if kata_search in p]
    else:
        filtered_options = POKEMON_LIST
        
    # フォーム1
    with st.form("form_step_1"):
        with st.container(height=300):
            selected_6 = st.pills(
                "相手のパーティ", 
                options=filtered_options, 
                selection_mode="multi",
                label_visibility="collapsed"
            )
        
        # 次へ進むボタン
        if st.form_submit_button("この6匹で決定 ＞"):
            if len(selected_6) > 0:
                st.session_state.opp_6 = selected_6
                st.session_state.step = 2
                st.rerun() # ステップ2へ画面を切り替え
            else:
                st.error("相手のポケモンを1匹以上選んでください。")

# ==========================================
# ステップ2：選出と結果の記録
# ==========================================
elif st.session_state.step == 2:
    st.subheader("② 選出と結果を記録")
    
    # 選んだ6匹の確認と戻るボタン
    st.write(f"**相手のパーティ:** {', '.join(st.session_state.opp_6)}")
    if st.button("＜ 相手の6匹を選び直す"):
        st.session_state.step = 1
        st.rerun()
        
    st.write("---")
    
    # フォーム2
    with st.form("form_step_2"):
        opp_4 = st.pills("相手の選出4匹", options=st.session_state.opp_6, selection_mode="multi")
        my_4 = st.pills("自分の選出4匹", options=MY_PARTY, selection_mode="multi")
        result = st.radio("勝敗", ["勝ち", "負け"], horizontal=True)
        
        # ※連動機能がないため、残ったポケモンの候補は両方のパーティ全員分を表示します
        last_pokemon_options = MY_PARTY + st.session_state.opp_6
        last_poke = st.pills("最後に場に残ったポケモン", options=last_pokemon_options, selection_mode="multi")
        
        # 記録ボタン
        if st.form_submit_button("スプレッドシートに保存"):
            if len(opp_4) > 0 and len(my_4) > 0:
                opp_6_str = ", ".join(st.session_state.opp_6)
                opp_4_str = ", ".join(opp_4)
                my_4_str = ", ".join(my_4)
                date_str = pd.Timestamp.now("Asia/Tokyo").strftime("%Y-%m-%d %H:%M")
                
                last_pokemon_str = ", ".join(last_poke) if len(last_poke) > 0 else "なし"
                current_party_str = ", ".join(sorted(MY_PARTY))
                
                # スプレッドシートに保存
                sheet.append_row([date_str, opp_6_str, opp_4_str, my_4_str, result, last_pokemon_str, current_party_str])
                
                # 完全にリセットしてステップ1に戻る
                st.session_state.opp_6 = []
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("相手の選出と自分の選出をそれぞれ1匹以上選んでください。")

# ==========================================
# 分析画面：選出率と履歴
# ==========================================
st.header("データ分析")

if st.button("データを最新に更新"):
    df = load_data()

if not df.empty:
    if "自分の6匹" in df.columns:
        # スプレッドシートの記録を、順番に依存しない形（名前順）に整える関数
        def sort_party_str(party_str):
            if pd.isna(party_str) or str(party_str).strip() == "":
                return ""
            # カンマで区切って、前後の空白を消して、並び替えて、再度結合する
            return ", ".join(sorted([p.strip() for p in str(party_str).split(",") if p.strip()]))
        
        # 比較用の新しい列「分析用パーティ」を一時的に作る
        df["分析用パーティ"] = df["自分の6匹"].apply(sort_party_str)
        
        # これまで使ったパーティの履歴を取得（空のデータは除外）
        party_history = [p for p in df["分析用パーティ"].unique() if p != ""]
        
        # 現在のパーティ（MY_PARTY）も同じルールで並び替える
        current_party_str = ", ".join(sorted(MY_PARTY))
        
        # 現在のパーティが履歴になければ追加
        if current_party_str not in party_history:
            party_history.insert(0, current_party_str)
            
        # プルダウンで分析対象を選択
        selected_party = st.selectbox(
            "▼ 分析するパーティを選択", 
            party_history, 
            index=party_history.index(current_party_str) if current_party_str in party_history else 0
        )
        
        # 並び替えた結果が一致するデータだけで絞り込み
        df_filtered = df[df["分析用パーティ"] == selected_party]
    else:
        df_filtered = df
        st.warning("※スプレッドシートに「自分の6匹」列がないため、全データを表示しています。")

    # 絞り込んだデータで集計・表示
    if not df_filtered.empty:
        st.subheader("自分のポケモンの選出割合")
        
        all_my_picks = []
        for picks in df_filtered["自分の選出"]:
            all_my_picks.extend(str(picks).split(", "))
        
        if all_my_picks:
            pick_counts = pd.Series(all_my_picks).value_counts().reset_index()
            pick_counts.columns = ['ポケモン', '選出回数']
            chart = alt.Chart(pick_counts).mark_bar().encode(
                x=alt.X('ポケモン', sort=None, title='ポケモン'),
                y=alt.Y('選出回数', title='選出回数'),
                tooltip=['ポケモン', '選出回数'] # マウスを乗せた時だけ数字が出るように設定
            )
            st.altair_chart(chart, use_container_width=True)

        win_count = len(df_filtered[df_filtered["勝敗"] == "勝ち"])
        total_count = len(df_filtered)
        st.write(f"**総対戦数:** {total_count} 戦 / **勝ち:** {win_count} 勝 / **勝率:** {(win_count/total_count)*100:.1f} %")

        st.subheader("スプレッドシートの記録")
        st.dataframe(df_filtered.sort_index(ascending=False))
    else:
        st.info("このパーティでの対戦記録はまだありません。")
else:
    st.info("まだスプレッドシートにデータがありません。")