# demo.py  –  keep suggesting new trend items until the user clicks 👍 Like
import streamlit as st, pandas as pd, random
from pathlib import Path
import json

CATALOG = pd.read_csv("catalog.csv")
TRENDS  = pd.read_csv("trends.csv")

# ---------- helpers ----------
def bmi(w, h_cm): return w / ((h_cm/100)**2)

def recommend_color(tone):
    palette = {
        "light":   ["Black","Navy","Mustard"],
        "neutral": ["White","Grey","Beige"],
        "warm":    ["White","Beige","Olive"],
        "cool":    ["White","Black","Navy"],
        "olive":   ["White","Beige","Red"],
    }
    return palette.get(tone, ["White"])[0]

# ---------- session initialisation ----------
if "trend_items" not in st.session_state:
    st.session_state.trend_items = []   # shuffled item_ids for the active trend
    st.session_state.trend_idx   = 0    # pointer into trend_items
    st.session_state.trend_tag   = None
    st.session_state.looping     = False

def start_trend_loop(keyword):
    """Initialise the list of items for a trend based on the search keyword."""
    st.session_state.trend_tag = (
        "athleisure" if "sneaker" in keyword.lower()
        else TRENDS.sort_values("popularity_score", ascending=False).iloc[0].style_tag
    )
    pool = CATALOG[CATALOG.style_tag == st.session_state.trend_tag]["item_id"].tolist()
    random.shuffle(pool)
    st.session_state.trend_items = pool
    st.session_state.trend_idx = 0
    st.session_state.looping = True

def current_trend_item():
    if not st.session_state.looping: return None
    if st.session_state.trend_idx >= len(st.session_state.trend_items):
        return None
    item_id = st.session_state.trend_items[st.session_state.trend_idx]
    return CATALOG[CATALOG.item_id == item_id].iloc[0]

# ---------- UI ----------
st.set_page_config(page_title="Fashion Demo", layout="wide")
st.title("مکان آنلاین")

kw = st.text_input("🔍  این‌جا دنبال کفش بگرد عزیزم (فعلا فقط اینو داریم: *sneakers*)")

# ==== 1) Search results ====
if kw:
    results = CATALOG[CATALOG.title.str.contains(kw, case=False)]
    st.subheader(f"ببین عمو چی پیدا کرده واسه‌ت : {len(results)} مورد")
    for _, r in results.iterrows():
        st.image(r.img_url, width=130)
        st.caption(f"**{r.title}** — ${r.price_usd}  @ {r.shop}")

    st.divider()

    # ==== 2) Personalisation choice ====
    choice = st.radio("👗  آیا می‌خوای برات شخصی‌سازی کنم؟",
                      ["نه من ماست‌م روئه", "با کمال میل"], index=0)

    if choice == "با کمال میل":
        c1, c2, c3 = st.columns(3)
        h = c1.number_input("بلندایت چه‌قدر است", 140, 210, 170)
        w = c2.number_input("کیلویی چند؟", 40, 140, 65)
        tone = c3.selectbox("میزان سیاهی", sorted(CATALOG.tone.unique()))

        personalised = results.copy()
        if bmi(w, h) > 27:
            personalised = personalised[~personalised.style_tag.str.contains("slim", case=False)]

        col_pref = recommend_color(tone)
        first = personalised[personalised.title.str.contains(col_pref, case=False)]
        pick  = first.iloc[[0]] if not first.empty else personalised.sample(1)
        p = pick.iloc[0]
        st.success(f"🎨 رنگ کفش پیش‌نهادی ما به تو دوست عزیز: **{col_pref}**")
        st.image(p.img_url, width=160, caption=f"{p.title} — ${p.price_usd}")

        # ==== 3) Start trend loop once ====
        if not st.session_state.looping:
            start_trend_loop(kw)

        # ==== 4) Show current trend item (loop) ====
        item = current_trend_item()
        if item is None:
            st.info("No more items in this trend. Thanks for the feedback!")
            st.session_state.looping = False
        else:
            st.divider()
            st.info(f"🔥 *به‌به ببین چه ترندی پیدا کردیم که به تو زیبا قامت میاد — {st.session_state.trend_tag}*")
            st.image(item.img_url, width=170,
                     caption=f"{item.title} — ${item.price_usd}")

            l_col, d_col = st.columns(2)
            if l_col.button("👍  دوست‌ش دارم", key=f"like_{item.item_id}"):
                st.success("خوش‌ت اومده‌ها. در خریدهای بعدی هم از این استفاده می‌کنیم واسه‌ت! 🙌")
                st.session_state.looping = False  # stop suggesting further items
            if d_col.button("👎  زشته مسخره", key=f"dislike_{item.item_id}"):
                st.warning(" باشه عزیزم، سلیقه‌ت رو درک می‌کنم. دکمه دیسلایک رو بمال تا آپشن‌های بیش‌تری ببینی. اگر ارور داد بازم بمال")
                st.session_state.trend_idx += 1   # move to next item
                st.experimental_rerun()           # refresh UI to show next
    else:
        # user chose "No thanks" → clear any ongoing loop
        st.info("خودت نخواستی شخصی‌سازی کنم. بیا همینا رو بخر.")
        st.session_state.looping = False
