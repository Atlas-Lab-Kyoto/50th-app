import streamlit as st
from google import genai

# ページ基本設定
st.set_page_config(
    page_title="フレンドフーズ 50周年特別商品 アイデア出しアシスト",
    page_icon="🎉",
    layout="centered"
)

# SecretsからGemini APIキーを取得してクライアントを初期化
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("⚠️ `.streamlit/secrets.toml` に `GEMINI_API_KEY` が設定されていません。")
    st.stop()

# ヘッダーエリア
st.title("🎉 50周年特別商品 アイデア出しアシスト")
st.caption("部門やキーワードを選ぶだけで、50周年にちなんだ商品企画のヒントや具体案をAIが一緒に考えます。")

# 部門と担当枠数の定義
DEPARTMENTS = {
    "青果部（目標: 6商品）": "青果部",
    "精肉部（目標: 7商品）": "精肉部",
    "鮮魚部（目標: 7商品）": "鮮魚部",
    "惣菜部（目標: 13商品）": "惣菜部",
    "パティスリー（目標: 3商品）": "パティスリー",
    "フロア部（目標: 14商品）": "フロア部",
    "部門横断（コラボ企画）": "部門横断（コラボ企画）"
}

# フォーム入力エリア
with st.form("idea_form"):
    st.subheader("💡 条件を選んでアイデアを生成")
    
    selected_dept_label = st.selectbox("担当部門を選択", list(DEPARTMENTS.keys()))
    dept_name = DEPARTMENTS[selected_dept_label]
    
    cut_angle = st.multiselect(
        "取り入れたい「50」の切り口（複数選択可）",
        [
            "「50」の形・数字（見た目やネーミング）",
            "50にちなんだ価格（505円、1050円、2500円など）",
            "50の数量・容量（50g、50個、50%増量、50種の素材など）",
            "50年前の流行・昔懐かしい味の現代風アレンジ",
            "創業当時の復刻・歴史を感じるストーリー",
            "50周年限定の超こだわり・プレミアム仕立て",
            "他部門とのコラボレーション"
        ],
        default=["「50」の形・数字（見た目やネーミング）"]
    )
    
    ingredient_or_theme = st.text_input(
        "使いたい食材・テーマ・気になっている商品（任意）",
        placeholder="例：京野菜、黒毛和牛、自家製焼き豚、特製醤油、昔ながらのお出汁 など"
    )
    
    free_note = st.text_area(
        "自由なメモ・やりたいことのニュアンス（任意）",
        placeholder="例：パートさんから「子どもも喜ぶド派手なものがいい」と意見があった、おつまみ系を強化したい、など"
    )

    submitted = st.form_submit_button("🔥 アイデアを生成する", use_container_width=True)

# 生成処理
if submitted:
    with st.spinner("フレンドフーズらしい、こだわり溢れる50周年アイデアを考えています..."):
        
        # プロンプトの組み立て
        prompt_text = f"""
あなたは京都の下鴨にあるこだわりのスーパーマーケット「フレンドフーズ」の優秀な商品開発コンサルタントです。
フレンドフーズ創業50周年を記念する「50周年特別商品（全50企画）」のアイデア出しをサポートしてください。

【フレンドフーズの理念・特徴】
・「ほんまもん」を追求し、商品の背景、生産者のこだわり、おいしさ、品質を最優先する。
・単なる安売りではなく、食の価値や美味しさの楽しさを伝える商品づくりを得意とする。

【企画条件】
・対象部門：{dept_name}
・取り入れたい切り口：{", ".join(cut_angle) if cut_angle else "自由提案"}
・使いたい食材・テーマ：{ingredient_or_theme if ingredient_or_theme else "指定なし（部門に合うものを提案してください）"}
・現場からのメモ・ニュアンス：{free_note if free_note else "特になし"}

【出力依頼】
上記条件を踏まえ、現場のスタッフがワクワクするような50周年特別商品の企画アイデアを「3案」提案してください。
各アイデアには以下の項目を含めてください：

1. **商品名案**（思わず手に取りたくなる、50周年らしさが伝わるネーミング）
2. **切り口**（どう「50」や「50周年」にかかっているか）
3. **商品概要・こだわりポイント**（フレンドフーズらしい仕立てや素材のポイント）
4. **想定価格帯**
5. **アピールポイント**（POPやnote記事で伝えられるストーリー）

親しみやすく、かつ現場のモチベーションが上がるポジティブなトーンで出力してください。
"""

        try:
            # Gemini 2.5 Flash モデルによる生成
            response = client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=prompt_text
            )
            
            st.success("🎉 アイデアが届きました！企画のヒントにしてみてください。")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

st.divider()
st.caption("※気に入ったアイデアがあれば、コピーして提出フォームや企画メモにご活用ください。")