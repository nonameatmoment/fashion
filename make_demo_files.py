#!/usr/bin/env python3
"""
make_demo_files.py  – v2
Creates   • catalog.csv   • trends.csv   • prefs.json
Run once, then start the Streamlit front-end with  `streamlit run demo.py`.
"""

import pandas as pd, json, random
from pathlib import Path

# ------------------------------------------------------------
# 1. CATALOG  – 10 items before + 8 sneakers in many colours
# ------------------------------------------------------------
catalog = [
    # --- previous 10 items (shortened titles for brevity) ----
    (1,  "White Linen Shirt",  "LinenCo",     49.99, "linen",     "light",   "women"),
    (2,  "Blue Denim Jacket",  "UrbanWear",   89.50, "denim",     "neutral", "women"),
    (3,  "Black Skinny Jeans", "DenimHub",    59.00, "slim",      "neutral", "women"),
    (4,  "Green Maxi Dress",   "BohoBoutique",72.25, "boho",      "olive",   "women"),
    (5,  "Red Graphic Tee",    "StreetMode",  24.99, "street",    "warm",    "women"),
    (6,  "Beige Chino Pants",  "SmartCasual", 54.75, "classic",   "neutral", "men"),
    (7,  "Navy Blazer",        "FormalHub",  110.00, "formal",    "cool",    "men"),
    (8,  "Grey Hoodie",        "AthleisureX", 39.99, "athleisure","neutral", "men"),
    (9,  "Floral Summer Dress","FemmeFlow",   65.50, "floral",    "light",   "women"),
    (10, "White Sneakers",     "KickStart",   59.95, "athleisure","light",   "men"),
    # --- NEW: sneaker palette --------------------------------
    (11, "Black Sneakers",     "SneakerHub",  62.00, "athleisure","neutral", "men"),
    (12, "Red Sneakers",       "KickStart",   61.00, "athleisure","warm",    "women"),
    (13, "Navy Sneakers",      "UrbanKicks",  60.00, "athleisure","cool",    "men"),
    (14, "Beige Sneakers",     "SmartCasual", 58.50, "athleisure","neutral", "women"),
    (15, "Olive Sneakers",     "BohoSneaks",  57.25, "athleisure","olive",   "women"),
    (16, "Grey Sneakers",      "AthleisureX", 59.75, "athleisure","neutral", "men"),
    (17, "Pastel Pink Sneakers","FemmeFlow",  63.00, "athleisure","light",   "women"),
    (18, "Mustard Sneakers",   "StreetMode",  60.50, "athleisure","warm",    "women"),
]

def pic(seed):  # quick image placeholder
    return f"https://picsum.photos/seed/{seed.replace(' ','-')}/200"

cat_df = pd.DataFrame(
    [(i,t,s,p,pic(t),g,tag,tone) for i,t,s,p,tag,tone,g in catalog],
    columns=["item_id","title","shop","price_usd","img_url",
             "gender","style_tag","tone"]
)
cat_df.to_csv("catalog.csv", index=False)
print("✓  catalog.csv  (with 8 colour-variant sneakers)")

# ------------------------------------------------------------
# 2. TRENDS  – keep simple, still 6 tags
# ------------------------------------------------------------
trends_df = pd.DataFrame(
    {"style_tag":["athleisure","linen","floral","street","denim","formal"],
     "popularity_score":[82,78,71,69,66,60],
     "season":["spring","summer","summer","year-round","year-round","fall"]}
)
trends_df.to_csv("trends.csv", index=False)
print("✓  trends.csv")

# ------------------------------------------------------------
# 3. PREF STORE (create only if absent)
# ------------------------------------------------------------
prefs = Path("prefs.json")
if not prefs.exists():
    json.dump({"demo_user":{"likes":[],"dislikes":[]}}, prefs.open("w"), indent=2)
    print("✓  prefs.json (fresh)")
else:
    print("•  prefs.json already present – untouched")
