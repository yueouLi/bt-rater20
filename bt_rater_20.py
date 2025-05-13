import streamlit as st
import pandas as pd

# 设置页面标题和布局
st.set_page_config(page_title="Backtranslation Rating - Rater 20", layout="centered")
st.title("📝 Simplification Back-Translation Evaluation - Rater 20")

# 读取 CSV 文件
df = pd.read_csv("bt_batch_20.csv", encoding="utf-8-sig")

rater_id = "rater20"

# 初始化评分记录
if "ratings_data" not in st.session_state:
    st.session_state.ratings_data = {}

# 打开评分准则说明
with st.expander("📘 View Manual Scoring Guidelines"):
    st.markdown("""
### 🎯 **Manual Scoring Protocol (1–5 Scale)**

This study introduces a human evaluation protocol for **multilingual sentence simplification (Chinese/German)**. Ratings are based on:

#### 1️⃣ **Meaning Preservation** (vs. original complex sentence)
> Does the simplification maintain the original meaning without adding, omitting, or distorting key content?

| Score | Description |
|---|---|
| **5** | Fully preserves meaning; no key info lost or altered |
| **4** | Minor shifts in meaning; core preserved |
| **3** | Partial meaning loss or distortion |
| **2** | Major omissions or misunderstandings |
| **1** | Contradicts or misses original intent |

🛑 _Common issues:_ addition, omission, entity confusion

---

#### 2️⃣ **Fluency** (language quality alone)
> Is the simplified sentence grammatically correct and natural?

| Score | Description |
|---|---|
| **5** | Fluent, native-like |
| **4** | Minor errors, easy to understand |
| **3** | Readable with noticeable issues |
| **2** | Hard to follow due to grammar |
| **1** | Unintelligible or broken syntax |

🛑 _Common issues:_ punctuation, verb forms, word order

---

#### 3️⃣ **Simplicity** (vs. original sentence)
> Has complexity been reduced structurally or lexically?

| Score | Description |
|---|---|
| **5** | Clearly easier to read, much simpler |
| **4** | Noticeably simpler |
| **3** | Slight improvement or same |
| **2** | Minimal simplification |
| **1** | Still complex or even harder |

💡 _Don’t confuse info loss (penalized under Meaning) with valid simplification._

---

#### 4️⃣ **Diversity** (vs. other references)
> Is the expression/style clearly different from other simplifications?

| Score | Description |
|---|---|
| **5** | Creative or unique structure/style |
| **4** | Distinct phrasing or tone |
| **3** | Some variation |
| **2** | Very similar wording |
| **1** | Nearly identical |

🔎 _Diversity ≠ quality. Use only when multiple references exist._
    """)

# 遍历全部样本（无分页）
for idx, row in df.iterrows():
    st.markdown(f"### 🔢 Sample {idx + 1}")
    st.markdown(f"**🟩 Source:**  \n{row['source']}")
    st.markdown(f"**🦁Sprache 1 Back-Translation:**  \n{row['bt_de']}")
    g_meaning = st.slider(f"Meaning (🦁) [{idx}]", 1, 5, 3, key=f"gm{idx}")
    g_fluency = st.slider(f"Fluency (🦁) [{idx}]", 1, 5, 3, key=f"gf{idx}")
    g_simplicity = st.slider(f"Simplicity (🦁) [{idx}]", 1, 5, 3, key=f"gs{idx}")
    g_diversity = st.slider(f"Diversity (🦁) [{idx}]", 1, 5, 3, key=f"gd{idx}")

    st.markdown(f"**🐮Sprache 2 Back-Translation:**  \n{row['bt_zh']}")
    c_meaning = st.slider(f"Meaning (🐮) [{idx}]", 1, 5, 3, key=f"cm{idx}")
    c_fluency = st.slider(f"Fluency (🐮) [{idx}]", 1, 5, 3, key=f"cf{idx}")
    c_simplicity = st.slider(f"Simplicity (🐮) [{idx}]", 1, 5, 3, key=f"cs{idx}")
    c_diversity = st.slider(f"Diversity (🐮) [{idx}]", 1, 5, 3, key=f"cd{idx}")

    st.session_state.ratings_data[idx] = {
        "rater_id": rater_id,
        "sample_id": idx + 1,
        "source": row["source"],
        "bt_de": row["bt_de"],
        "bt_zh": row["bt_zh"],
        "g_meaning": g_meaning,
        "g_fluency": g_fluency,
        "g_simplicity": g_simplicity,
        "g_diversity": g_diversity,
        "c_meaning": c_meaning,
        "c_fluency": c_fluency,
        "c_simplicity": c_simplicity,
        "c_diversity": c_diversity,
    }

# 显示评分进度
st.markdown("---")
st.markdown(f"📊 Progress: {len(st.session_state.ratings_data)} / {len(df)} samples rated.")

# 下载按钮
if st.button("⬇️ Download Ratings CSV"):
    all_ratings_df = pd.DataFrame.from_dict(st.session_state.ratings_data, orient="index")
    csv_bytes = all_ratings_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
    st.download_button(
        label="📥 Click here to download",
        data=csv_bytes,
        file_name=f"bt_ratings_{rater_id}.csv",
        mime="text/csv"
    )
