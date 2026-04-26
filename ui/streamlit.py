import streamlit as st
import requests
import time

API_URL = "https://advance-rag-system-chatbot-tawj.onrender.com"

# Wake up Render backend on page load to avoid cold start on first query
try:
    requests.get(f"{API_URL}/health", timeout=5)
except:
    pass

st.set_page_config(
    page_title="Advanced RAG Assistant",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

#SIDEBAR
with st.sidebar:
    st.title("⚙️ Controls")

    show_query = st.toggle("Show Improved Query", True)
    show_sources = st.toggle("Show Sources", True)

    st.markdown("---")
    st.markdown("## 📂 Upload PDF")
    st.caption("Max file size: 5MB")

    uploaded_file = st.file_uploader("Upload document", type=["pdf"])

    if uploaded_file:
        with st.spinner("Uploading..."):

            files = {
                "file": (uploaded_file.name, uploaded_file, "application/pdf")
            }

            try:
                res = requests.post(f"{API_URL}/upload", files=files, timeout=30)

                if res.status_code == 200:
                    res_json = res.json()

                    # Show error returned by backend (e.g. file too large)
                    if "error" in res_json:
                        st.error(f"❌ {res_json['error']}")
                    else:
                        st.success("✅ Uploaded! Processing in background...")

                        status_placeholder = st.empty()
                        start_wait = time.time()

                        while True:
                            # Timeout after 2 minutes prevents infinite spinner
                            if time.time() - start_wait > 120:
                                status_placeholder.error(
                                    "⏱️ Processing is taking too long. "
                                    "Try a smaller PDF (under 2MB)."
                                )
                                break

                            try:
                                response = requests.get(
                                    f"{API_URL}/status",
                                    params={"filename": uploaded_file.name},
                                    timeout=10
                                )

                                # Guard against empty/crashed backend response
                                if response.text.strip() == "":
                                    status_placeholder.error(
                                        "❌ Backend crashed or restarted. "
                                        "Please re-upload your file."
                                    )
                                    break

                                status_res = response.json()
                                status = status_res.get("status")

                            except requests.exceptions.Timeout:
                                status_placeholder.warning("⏳ Backend is slow, still waiting...")
                                time.sleep(2)
                                continue
                            except Exception as e:
                                status_placeholder.error(f"❌ Status check failed: {str(e)}")
                                break

                            if status == "processing":
                                status_placeholder.info("⏳ Processing document...")
                                time.sleep(1)

                            elif status in ("done", "ready_partial"):
                                status_placeholder.success("✅ Ready to query!")
                                break

                            elif status and "error" in str(status):
                                status_placeholder.error(f"❌ {status}")
                                break

                            else:
                                time.sleep(1)

                else:
                    st.error("❌ Upload failed. Backend returned an error.")

            except requests.exceptions.Timeout:
                st.error("❌ Upload timed out. Backend may be sleeping — try again in 30 seconds.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    st.markdown("---")
    st.markdown("## 📁 Documents")

    try:
        response = requests.get(f"{API_URL}/documents", timeout=10)
        if response.text.strip():
            docs = response.json().get("documents", [])
            for doc in docs:
                st.write(f"📄 {doc}")
        else:
            st.warning("Backend not reachable")
    except:
        st.warning("Could not fetch documents")

# SESSION STATE 
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#  HEADER
st.title("🤖 Advanced RAG Assistant")
st.caption("Fast • Intelligent • Streaming RAG System")

#  CHAT HISTORY 
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(chat["query"])
    with st.chat_message("assistant"):
        st.markdown(chat["answer"])

#  INPUT 
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
                stream=True,
                timeout=60
            ) as r:
                for chunk in r.iter_content(chunk_size=20):
                    if chunk:
                        text = chunk.decode("utf-8")
                        full_text += text
                        placeholder.markdown(full_text + "▌")

        except requests.exceptions.Timeout:
            st.error("⏱️ Response timed out. Backend may be overloaded.")
            st.stop()
        except Exception:
            st.error("❌ Backend not reachable. Please try again.")
            st.stop()

        placeholder.markdown(full_text)

    latency = round(time.time() - start, 2)

    # /ask reads from cache instant, no second pipeline run
    try:
        meta_response = requests.get(
            f"{API_URL}/ask",
            params={"query": query},
            timeout=10
        )
        meta = meta_response.json() if meta_response.text.strip() else {}
    except:
        meta = {}

    col1, col2 = st.columns(2)
    col1.metric("⏱ Response Time", f"{latency}s")
    col2.metric("📄 Sources", len(meta.get("sources", [])))

    if show_query:
        with st.expander("🔁 Improved Query"):
            st.write(meta.get("improved_query", "N/A"))

    if show_sources:
        with st.expander("📚 Sources"):
            for src in meta.get("sources", []):
                st.json(src)

    st.session_state.chat_history.append({
        "query": query,
        "answer": full_text
    })