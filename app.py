import streamlit as st
import faiss
import pickle
import numpy as np
import re

from openai import OpenAI

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Sportomic Podcast Q&A Bot",
    page_icon="🎙️",
    layout="wide"
)

# ======================================
# HELPERS
# ======================================

def seconds_to_hms(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{secs:02d}"
    )

# ======================================
# LOAD ENV
# ======================================


if "OPENAI_API_KEY" not in st.secrets:
    st.error("OPENAI_API_KEY not found in Streamlit secrets.")
    st.stop()

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

VIDEO_ID = "Rni7Fz7208c"
TOP_K = 5

# ======================================
# LOAD INDEX
# ======================================

@st.cache_resource
def load_resources():

    index = faiss.read_index(
        "embeddings/faiss_index.bin"
    )

    with open(
        "embeddings/chunks.pkl",
        "rb"
    ) as f:
        chunks = pickle.load(f)

    return index, chunks

index, chunks = load_resources()

# ======================================
# UI
# ======================================

st.title("🎙️ Podcast Q&A Bot")
st.markdown("""
This AI-powered Podcast Q&A Bot allows users to ask questions about the
Elon Musk × Nikhil Kamath podcast and instantly receive:

✅ Context-aware answers

✅ Supporting transcript evidence

✅ Direct timestamp references

✅ One-click navigation to the relevant video section
""")

question = st.text_input(
    "Ask a question",
    placeholder="What is first principles thinking?"
)

# ======================================
# QUERY
# ======================================

if st.button("Ask") and question:

    with st.spinner("Searching podcast..."):

        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=question
        )

        query_embedding = np.array(
            [embedding_response.data[0].embedding],
            dtype=np.float32
        )

        distances, indices = index.search(
            query_embedding,
            TOP_K
        )

        retrieved_chunks = [
            chunks[idx]
            for idx in indices[0]
        ]

        # -------------------------------
        # GPT chooses best chunk
        # -------------------------------

        chunk_descriptions = []

        for i, chunk in enumerate(retrieved_chunks):

            chunk_descriptions.append(
                f"""
Chunk {i+1}

Timestamp:
{seconds_to_hms(chunk['start'])}

Text:
{chunk['text']}
"""
            )

        selection_prompt = f"""
Question:
{question}

Choose the chunk that BEST answers the question.

Return only the chunk number.

{''.join(chunk_descriptions)}
"""

        selection = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": selection_prompt
                }
            ]
        )

        response_text = (
            selection.choices[0]
            .message.content
        )

        match = re.search(
            r"\d+",
            response_text
        )

        if match:
            selected_index = (
                int(match.group()) - 1
            )
        else:
            selected_index = 0

        selected_index = max(
            0,
            min(
                selected_index,
                len(retrieved_chunks) - 1
            )
        )

        best_chunk = retrieved_chunks[
            selected_index
        ]

        # -------------------------------
        # FINAL ANSWER
        # -------------------------------

        answer_prompt = f"""
You are a podcast assistant.

Answer ONLY using the transcript.

Question:
{question}

Transcript:
{best_chunk["text"]}

Return exactly:

Answer:
<answer>

Evidence:
<direct quote>

Explanation:
<short explanation>
"""

        answer = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": answer_prompt
                }
            ]
        )

        timestamp = best_chunk["start"]

        youtube_link = (
            f"https://www.youtube.com/watch?v={VIDEO_ID}"
            f"&t={int(timestamp)}s"
        )

    # ======================================
    # DISPLAY RESULTS
    # ======================================

    st.success("Answer Found")

    st.subheader("Answer")

    st.write(
        answer.choices[0]
        .message.content
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Timestamp",
            seconds_to_hms(timestamp)
        )

    with col2:
        st.link_button(
            "Open Video",
            youtube_link
        )

    with st.expander(
        "Retrieved Transcript"
    ):
        st.write(best_chunk["text"])