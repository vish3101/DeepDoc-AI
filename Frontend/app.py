import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"  # Change this if deployed

st.set_page_config(page_title="DeepDoc AI", layout="wide")

st.title("DeepDoc AI")
st.subheader("An intelligent document Q&A assistant")

st.sidebar.title("Navigation")
option = st.sidebar.radio("Go to", ["Upload PDF", "Ask Query", "List PDFs"])

if option == "Upload PDF":
    st.subheader("Upload your PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file and st.button("Submit to Backend"):
        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        try:
            response = requests.post(f"{API_BASE_URL}/upload-pdf", files=files)
            if response.status_code in (200,201):
                st.success("File successfully uploaded to backend.")
            else:
                st.error(f"Upload failed: {response.text}")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")

elif option == "Ask Query":
    st.subheader("Ask a Question")
    pdf_name=st.text_input("Enter PDF name:")
    query = st.text_input("Type your question:")
    if st.button("Submit Query"):
        try:
            payload = {
                "pdf_name": pdf_name,
                "question": query
            }
            response = requests.post(f"{API_BASE_URL}/ask", json=payload)
            if response.status_code == 200:
                st.write(f"**Answer:** {response.json().get('answer', 'No answer returned.')}")
            else:
                st.error(f"Query failed: {response.text}")
        except Exception as e:
            st.error(f"Error contacting backend: {e}")

elif option == "List PDFs":
    st.subheader("📚 Your Uploaded PDFs")
    try:
        response = requests.get(f"{API_BASE_URL}/list-pdfs")
        if response.status_code == 200:
            pdfs = response.json().get("pdf_files", [])
            if pdfs:
                for doc in pdfs:
                    st.markdown(f"- **{doc}**")
            else:
                st.info("No PDFs found.")
        else:
            st.error(f"Failed to fetch PDFs: {response.text}")
    except Exception as e:
        st.error(f"Error contacting backend: {e}")
