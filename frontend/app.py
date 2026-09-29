import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000/api/generate-document"
DOCX_API_URL = "http://127.0.0.1:8000/api/download-docx"
PDF_API_URL = "http://127.0.0.1:8000/api/download-pdf"


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

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


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""


# --------------------------------------------------
# TITLE
# --------------------------------------------------

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


# --------------------------------------------------
# DOCUMENT TYPE
# --------------------------------------------------

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


# --------------------------------------------------
# USER DETAILS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📝 Enter Document Details</div>',
    unsafe_allow_html=True
)

details = st.text_area(
    "Describe the required details",
    placeholder=(
        "Example:\n"
        "Party A: ABC Company\n"
        "Party B: John\n"
        "Purpose: Confidential business information"
    ),
    height=220
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if st.button(
    "⚡ Generate Document",
    use_container_width=True
):

    if not details.strip():

        st.warning(
            "Please enter the document details."
        )

    else:

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "document_type": document_type,
                        "details": details
                    },
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.generated_document = (
                        result["document"]
                    )

                    st.session_state.document_type = (
                        document_type
                    )

                    st.success(
                        "Document generated successfully! ✅"
                    )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to LegalEase AI backend. "
                    "Please make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Request timed out. "
                    "Gemini API may be unavailable or rate-limited."
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )


# --------------------------------------------------
# DISPLAY GENERATED DOCUMENT
# --------------------------------------------------

if st.session_state.generated_document:

    st.markdown(
        '<div class="section-title">📑 Generated Document</div>',
        unsafe_allow_html=True
    )

    edited_document = st.text_area(
        "Review / Edit Document",
        value=st.session_state.generated_document,
        height=600,
        key="document_editor"
    )

    st.session_state.generated_document = edited_document


    # --------------------------------------------------
    # DOWNLOAD SECTION
    # --------------------------------------------------

    st.markdown(
        '<div class="section-title">⬇️ Download Document</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # TXT DOWNLOAD
    # --------------------------------------------------

    st.download_button(
        label="📝 Download TXT",
        data=edited_document,
        file_name="LegalEase_Document.txt",
        mime="text/plain",
        use_container_width=True
    )


    # --------------------------------------------------
    # DOCX DOWNLOAD
    # --------------------------------------------------

    try:

        docx_response = requests.post(
            DOCX_API_URL,
            json={
                "document": edited_document
            },
            timeout=30
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

            st.error(
                f"DOCX API Error: "
                f"{docx_response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to DOCX API."
        )

    except Exception as e:

        st.error(
            f"DOCX error: {e}"
        )


    # --------------------------------------------------
    # PDF DOWNLOAD
    # --------------------------------------------------

    try:

        pdf_response = requests.post(
            PDF_API_URL,
            json={
                "document": edited_document
            },
            timeout=30
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

            st.error(
                f"PDF API Error: "
                f"{pdf_response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to PDF API."
        )

    except Exception as e:

        st.error(
            f"PDF error: {e}"
        )


    # --------------------------------------------------
    # CREATE NEW DOCUMENT
    # --------------------------------------------------

    st.markdown("---")

    if st.button(
        "🔄 Create New Document",
        use_container_width=True
    ):

        st.session_state.generated_document = ""
        st.session_state.document_type = ""

        st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="disclaimer">
    ⚠️ LegalEase AI generates draft documents for informational purposes.
    Review the document with a qualified legal professional before relying on it.
    </div>
    """,
    unsafe_allow_html=True
)