import streamlit as st
import requests
import time

API_URL = "https://advance-rag-system-chatbot-tawj.onrender.com"

# ADDED: Wake up Render backend on page load to avoid cold start delay
try:
    requests.get(f"{API_URL}/health", timeout=5)
except:
    pass

st.set_page_config(
    page_title="Advanced RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

# STYLING
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("⚙️ Controls")

    show_query = st.toggle("Show Improved Query", True)
    show_sources = st.toggle("Show Sources", True)

    st.markdown("---")
    st.markdown("## 📂 Upload PDF")

    uploaded_file = st.file_uploader("Upload document", type=["pdf"])

    if uploaded_file:
        with st.spinner("Uploading..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }

            try:
                res = requests.post(f"{API_URL}/upload", files=files)

                if res.status_code == 200:
                    st.success("✅ Uploaded! Processing in background...")

                    status_placeholder = st.empty()

                    while True:
                        status_res = requests.get(
                            f"{API_URL}/status",
                            params={"filename": uploaded_file.name}
                        ).json()

                        status = status_res.get("status")

                        if status == "processing":
                            status_placeholder.info("⏳ Processing document...")
                            time.sleep(1)

                        elif status == "done":
                            status_placeholder.success("✅ Ready to query!")
                            break

                        elif "error" in str(status):
                            status_placeholder.error(status)
                            break

                        else:
                            time.sleep(1)

                else:
                    st.error("❌ Upload failed")

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown("---")

    st.markdown("## 📁 Documents")

    try:
        docs = requests.get(f"{API_URL}/documents").json().get("documents", [])

        for doc in docs:
            st.write(f"📄 {doc}")

    except:
        st.warning("Could not fetch documents")

# SESSION
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Store metadata in session state to avoid double API call
if "last_meta" not in st.session_state:
    st.session_state.last_meta = {}

# HEADER
st.title("🤖 Advanced RAG Assistant")
st.caption("Fast • Intelligent • Streaming RAG System")

# CHAT
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["query"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])

# INPUT
query = st.chat_input("Ask your question related to uploaded pdf...")

if query:
    with st.chat_message("user"):
        st.markdown(query)

    start = time.time()

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_text = ""

        try:
            with requests.get(
                f"{API_URL}/ask-stream",
                params={"query": query},
                stream=True
            ) as r:

                for chunk in r.iter_content(chunk_size=20):
                    if chunk:
                        text = chunk.decode("utf-8")
                        full_text += text
                        placeholder.markdown(full_text + "▌")

        except:
            st.error("Backend not reachable")
            st.stop()

        placeholder.markdown(full_text)

    latency = round(time.time() - start, 2)

    # /ask reads from cache (no second pipeline run)
    meta = requests.get(f"{API_URL}/ask", params={"query": query}).json()

    col1, col2 = st.columns(2)
    col1.metric("⏱ Response Time", f"{latency}s")
    col2.metric("📄 Sources", len(meta.get("sources", [])))

    if show_query:
        with st.expander("🔁 Improved Query"):
            st.write(meta.get("improved_query", ""))

    if show_sources:
        with st.expander("📚 Sources"):
            for src in meta.get("sources", []):
                st.json(src)

    st.session_state.chat_history.append({
        "query": query,
        "answer": full_text
    })