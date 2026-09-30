import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/api/generate-document"
DOCX_API_URL = "http://127.0.0.1:8000/api/download-docx"
PDF_API_URL = "http://127.0.0.1:8000/api/download-pdf"


st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .disclaimer {
        text-align: center;
        font-size: 13px;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# SESSION STATE
# -----------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""


# -----------------------------
# TITLE
# -----------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True
)

st.info(
    "Generate a draft legal document using AI. "
    "Review and customize the document before use."
)


# -----------------------------
# DOCUMENT TYPE
# -----------------------------

st.markdown(
    '<div class="section-title">📄 Select Document Type</div>',
    unsafe_allow_html=True
)

document_type = st.selectbox(
    "Document Type",
    [
        "Non-Disclosure Agreement (NDA)",
        "Employment Contract",
        "Residential Lease Agreement"
    ]
)


# -----------------------------
# USER DETAILS
# -----------------------------

st.markdown(
    '<div class="section-title">📝 Enter Document Details</div>',
    unsafe_allow_html=True
)

details = st.text_area(
    "Document Details",
    height=180,
    placeholder=(
        "Example:\n"
        "Party A: ABC Technologies Pvt Ltd\n"
        "Party B: John Kumar\n"
        "Purpose: Confidential business information\n"
        "Effective Date: 29 September 2026\n"
        "Confidentiality Period: 2 years"
    )
)


# -----------------------------
# GENERATE DOCUMENT
# -----------------------------

if st.button("⚡ Generate Document", use_container_width=True):

    if not details.strip():
        st.warning("Please enter the document details.")
    else:

        payload = {
            "document_type": document_type,
            "details": details
        }

        try:

            with st.spinner("Generating legal document..."):

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=120
                )

            if response.status_code == 200:

                data = response.json()

                generated_document = data.get("document", "")

                st.session_state.generated_document = generated_document
                st.session_state.document_type = document_type

                st.success("Document generated successfully! ✅")

            else:

                st.error(
                    f"API Error: {response.status_code}\n\n"
                    f"{response.text}"
                )

        except requests.exceptions.RequestException as e:

            st.error(f"Unable to connect to backend: {e}")


# -----------------------------
# GENERATED DOCUMENT
# -----------------------------

if st.session_state.generated_document:

    st.markdown(
        '<div class="section-title">📑 Generated Document</div>',
        unsafe_allow_html=True
    )

    edited_document = st.text_area(
        "Review and edit your document",
        value=st.session_state.generated_document,
        height=500
    )

    st.session_state.generated_document = edited_document


    # -------------------------
    # DOWNLOAD DOCUMENT
    # -------------------------

    st.markdown(
        '<div class="section-title">⬇️ Download Document</div>',
        unsafe_allow_html=True
    )


    col1, col2, col3 = st.columns(3)


    # -------------------------
    # DOCX
    # -------------------------

    with col1:

        try:

            docx_response = requests.post(
                DOCX_API_URL,
                json={"document": edited_document},
                timeout=60
            )

            if docx_response.status_code == 200:

                st.download_button(
                    label="📄 Download DOCX",
                    data=docx_response.content,
                    file_name="LegalEase_Document.docx",
                    mime=(
                        "application/vnd.openxmlformats-officedocument."
                        "wordprocessingml.document"
                    ),
                    use_container_width=True
                )

            else:

                st.error("DOCX generation failed.")

        except Exception as e:

            st.error(f"DOCX error: {e}")


    # -------------------------
    # PDF
    # -------------------------

    with col2:

        try:

            pdf_response = requests.post(
                PDF_API_URL,
                json={"document": edited_document},
                timeout=60
            )

            if pdf_response.status_code == 200:

                st.download_button(
                    label="📕 Download PDF",
                    data=pdf_response.content,
                    file_name="LegalEase_Document.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

            else:

                st.error("PDF generation failed.")

        except Exception as e:

            st.error(f"PDF error: {e}")


    # -------------------------
    # TXT
    # -------------------------

    with col3:

        st.download_button(
            label="📝 Download TXT",
            data=edited_document,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True
        )


# -----------------------------
# DISCLAIMER
# -----------------------------

st.markdown(
    """
    <div class="disclaimer">
    ⚠️ LegalEase AI generates draft documents for informational purposes.
    Review the document with a qualified legal professional before relying on it.
    </div>
    """,
    unsafe_allow_html=True
)