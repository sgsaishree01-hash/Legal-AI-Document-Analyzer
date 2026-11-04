import os
import base64
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PyPDF2 import PdfReader


st.set_page_config(
    page_title="SMART LEGAL AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY is missing. Check your .env file.")
    st.stop()

client = genai.Client(api_key=api_key)
MODEL_NAME = "gemini-3.8-flash"

image_path = Path("image.jpg")

background_style = """
background: radial-gradient(
    circle at top right,
    #17345e 0%,
    #08162d 48%,
    #050d1b 100%
);
"""

if image_path.exists():
    encoded_image = base64.b64encode(
        image_path.read_bytes()
    ).decode("utf-8")

    background_style = f"""
        background-image:
            linear-gradient(
                rgba(4,15,34,.93),
                rgba(4,15,34,.95)
            ),
            url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """

st.markdown(
    f"""
    <style>
    * {{
        box-sizing: border-box;
    }}

    [data-testid="stSidebar"],
    [data-testid="collapsedControl"],
    header,
    #MainMenu,
    footer {{
        visibility: hidden;
        height: 0;
    }}

    .stApp {{
        min-height: 100vh;
        {background_style}
    }}

    /* Reduce unused space at the top */
    .main .block-container {{
        max-width: 1420px;
        padding: 0px 34px 18px !important;
    }}

    [data-testid="stMainBlockContainer"] {{
        padding-top: 0px !important;
    }}

    /* Remove extra space between Streamlit elements */
    [data-testid="stVerticalBlock"] {{
        gap: 0.55rem;
    }}

    .brand-row {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        padding: 0;
        margin: 0 0 30px;
        min-height: 0;
    }}

    .brand {{
        color: #f8fbff;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: .5px;
        line-height: 1.3;
    }}

    .brand .brand-accent {{
        color: #70aaff;
    }}

    .hero-title {{
        color: #70aaff;
        font-size: clamp(26px, 3vw, 36px);
        font-weight: 800;
        text-align: center;
        line-height: 1.25;
        margin: 0 0 14px;
    }}

    .hero-description {{
        color: #c5d1e2;
        font-size: 16px;
        line-height: 1.6;
        text-align: center;
        margin: 0 0 24px;
    }}

    .section-heading {{
        color: #f7faff;
        font-size: 19px;
        font-weight: 760;
        line-height: 1.4;
        margin: 0 0 5px;
    }}

    .section-subtitle {{
        color: #b7c5d9;
        font-size: 12px;
        line-height: 1.65;
        margin: 0 0 14px;
    }}

    [data-testid="stSelectbox"] label,
    [data-testid="stFileUploader"] label,
    [data-testid="stTextArea"] label {{
        color: #e4ecf8 !important;
        font-size: 13px !important;
        font-weight: 650 !important;
    }}

    [data-testid="stSelectbox"] > div > div {{
        background: #f8fafc !important;
        border-radius: 10px !important;
        border: 1px solid #dbe4f0 !important;
        color: #14213a !important;
        min-height: 44px;
    }}

    [data-testid="stFileUploader"] section {{
        background: rgba(248,250,252,.98);
        border: 1px dashed #b9c9df;
        border-radius: 12px;
        padding: 12px;
    }}

    [data-testid="stFileUploader"] section * {{
        color: #263750;
    }}

    [data-testid="stTextArea"] textarea {{
        min-height: 145px !important;
        border-radius: 10px !important;
        background: #ffffff !important;
        color: #152238 !important;
        border: 1px solid #d5deea !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
        resize: vertical !important;
    }}

    [data-testid="stTextArea"] textarea::placeholder {{
        color: #8795a8 !important;
    }}

    div.stButton > button {{
        width: 100%;
        min-height: 47px;
        border-radius: 10px;
        border: 1px solid #4b8bff;
        background: linear-gradient(135deg, #3478f6, #2463d9);
        color: #ffffff;
        font-size: 13px;
        font-weight: 750;
        letter-spacing: .2px;
        box-shadow: 0 8px 22px rgba(37,99,235,.18);
        transition: filter .15s ease;
    }}

    div.stButton > button:hover {{
        filter: brightness(1.08);
        color: #ffffff;
        border-color: #8ab6ff;
    }}

    .report-topline {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin: 0 0 12px;
    }}

    .report-label {{
        display: inline-flex;
        align-items: center;
        gap: 7px;
        background: rgba(125,211,167,.10);
        color: #b8f0d0;
        border: 1px solid rgba(125,211,167,.24);
        padding: 6px 10px;
        border-radius: 999px;
        font-size: 10px;
        font-weight: 750;
        letter-spacing: .4px;
    }}

    .st-key-report_card {{
        min-height: 420px;
        max-height: 560px;
        overflow-y: auto;
        overflow-x: hidden;
        background: #ffffff !important;
        border: 1px solid #dce5f0;
        border-radius: 14px;
        padding: 21px 24px;
        color: #1e293b !important;
        box-shadow: 0 12px 30px rgba(0,0,0,.10);
    }}

    .st-key-report_card > div {{
        background: transparent !important;
    }}

    .st-key-report_card h1,
    .st-key-report_card h2,
    .st-key-report_card h3,
    .st-key-report_card h4,
    .st-key-report_card p,
    .st-key-report_card li,
    .st-key-report_card strong,
    .st-key-report_card em,
    .st-key-report_card span {{
        color: #1e293b !important;
    }}

    .st-key-report_card h1,
    .st-key-report_card h2 {{
        font-size: 18px !important;
        font-weight: 800 !important;
        border-bottom: 1px solid #e4eaf2;
        padding-bottom: 8px;
        margin-top: 12px;
    }}

    .st-key-report_card h3,
    .st-key-report_card h4 {{
        font-size: 15px !important;
        font-weight: 750 !important;
        margin-top: 13px;
    }}

    .st-key-report_card p,
    .st-key-report_card li {{
        font-size: 13px !important;
        line-height: 1.75 !important;
    }}

    .st-key-report_card ul,
    .st-key-report_card ol {{
        padding-left: 22px;
    }}

    .st-key-report_card::-webkit-scrollbar {{
        width: 7px;
    }}

    .st-key-report_card::-webkit-scrollbar-thumb {{
        background: #cbd5e1;
        border-radius: 10px;
    }}

    .empty-report {{
        min-height: 420px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: rgba(255,255,255,.98);
        border: 1px dashed #c5d2e2;
        border-radius: 14px;
        padding: 26px;
        box-shadow: 0 12px 30px rgba(0,0,0,.08);
    }}

    .empty-report-icon {{
        width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 14px;
        border-radius: 17px;
        background: #edf4ff;
        font-size: 27px;
    }}

    .empty-report-title {{
        color: #24334a;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 8px;
    }}

    .empty-report-text {{
        max-width: 310px;
        color: #65758c;
        font-size: 12px;
        line-height: 1.8;
    }}

    .stDownloadButton {{
        margin-top: 12px;
    }}

    .stDownloadButton button {{
        width: 100%;
        min-height: 43px;
        border-radius: 10px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid #cbd8e8;
        background: #f8fbff;
        color: #1e3a5f;
    }}

    [data-testid="stAlert"] {{
        border-radius: 10px;
        font-size: 13px;
    }}

    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 0px 15px 18px !important;
        }}

        .brand-row {{
            margin-bottom: 22px;
        }}

        .brand {{
            font-size: 19px;
        }}

        .hero-title {{
            font-size: 26px;
        }}

        .hero-description {{
            font-size: 14px;
            margin-bottom: 22px;
        }}

        .st-key-report_card {{
            min-height: 320px;
            max-height: 460px;
            padding: 16px;
        }}

        .empty-report {{
            min-height: 320px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# Application header
st.markdown(
    """
    <div class="brand-row">
        <div class="brand">
            ⚖️ <span class="brand-accent">SMART</span> LEGAL AI
        </div>
    </div>

    <div class="hero-title">
        Smart Legal Document Analysis
    </div>

    <div class="hero-description">
        Upload a legal document to extract important details,
        identify potential risks and generate a structured AI report.
    </div>
    """,
    unsafe_allow_html=True,
)


if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


left, right = st.columns([0.92, 1.08], gap="large")


# Document input
with left:
    st.markdown(
        """
        <div class="section-heading">Document Input</div>
        <div class="section-subtitle">
            Choose the document category, then upload a PDF or paste its content.
        </div>
        """,
        unsafe_allow_html=True,
    )

    document_type = st.selectbox(
        "Document category",
        [
            "Sale Deed",
            "Lease Agreement",
            "Employment Contract",
            "Partnership Deed",
        ],
    )

    uploaded_file = st.file_uploader(
        "Upload legal document (PDF)",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned PDFs may require OCR.",
    )

    document = ""

    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            page_texts = []

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    page_texts.append(page_text.strip())

            document = "\n\n".join(page_texts).strip()

            if document:
                st.success(
                    f"PDF ready · {len(reader.pages)} page(s)"
                )
            else:
                st.warning(
                    "No readable text was found in this PDF. "
                    "Try a text-based PDF or paste the document text below."
                )

        except Exception:
            st.error(
                "We couldn't read this PDF. Please check the file and try again."
            )

    manual_text = st.text_area(
        "Or paste document text",
        height=145,
        placeholder="Paste the legal document text here...",
    )

    if manual_text.strip():
        document = manual_text.strip()

    analyze = st.button(
        "ANALYSE DOCUMENT WITH AI",
        use_container_width=True,
    )


# Analysis report
with right:
    st.markdown(
        """
        <div class="section-heading">Analysis Report</div>
        <div class="section-subtitle">
            Review extracted details, potential concerns, and points to discuss
            with a qualified professional.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if analyze:
        if not document.strip():
            st.warning(
                "Upload a readable PDF or paste legal document text first."
            )

        else:
            st.session_state.analysis_result = None

            prompt = f"""
You are an AI assistant helping a reader understand a legal document.

Selected document category: {document_type}.

Create a professional report in clear Markdown with these sections:

## DOCUMENT DETAILS
- Document Type
- Parties Involved
- Important Dates
- Money / Amount
- Duration
- Property / Subject

## POTENTIAL LEGAL RISKS
Identify possible risks, missing clauses, unclear conditions, unusual terms,
and items that may need professional review.

Distinguish confirmed omissions from information that cannot be verified
from the supplied text.

## AI SUGGESTIONS
Give practical points to clarify or review.

## SIMPLE ENGLISH SUMMARY
Explain the document in simple English for a non-lawyer.

Requirements:
- Use only information supported by the supplied document.
- Do not invent names, dates, amounts, or clauses.
- Clearly state when information is missing or unclear.
- Do not claim that a document is legally valid or invalid.
- Do not provide final legal advice.
- If the text is incomplete, say the analysis is limited to the available text.
- End by recommending review by a qualified legal professional.

DOCUMENT TEXT:

{document}
"""

            try:
                with st.spinner(
                    "Reviewing the document and preparing your report..."
                ):
                    response = None
                    max_attempts = 3

                    for attempt in range(max_attempts):
                        try:
                            response = client.models.generate_content(
                                model=MODEL_NAME,
                                contents=prompt,
                            )
                            break

                        except Exception as api_error:
                            error_text = str(api_error).lower()

                            is_temporary = any(
                                term in error_text
                                for term in (
                                    "503",
                                    "unavailable",
                                    "429",
                                    "resource_exhausted",
                                )
                            )

                            if (
                                not is_temporary
                                or attempt == max_attempts - 1
                            ):
                                raise

                            time.sleep(2 ** (attempt + 1))

                result = getattr(response, "text", None)

                if result and result.strip():
                    st.session_state.analysis_result = result.strip()
                else:
                    st.error(
                        "The AI returned an empty report. Please try again."
                    )

            except Exception as error:
                error_text = str(error).lower()

                if "503" in error_text or "unavailable" in error_text:
                    st.error(
                        "Gemini is temporarily busy (503 UNAVAILABLE). "
                        "Please wait a little and try again."
                    )

                elif (
                    "429" in error_text
                    or "resource_exhausted" in error_text
                ):
                    st.error(
                        "The Gemini API has reached a request or usage limit. "
                        "Please wait and check your API quota if the problem continues."
                    )

                else:
                    st.error(
                        "AI analysis couldn't be completed. Please try again."
                    )

                    with st.expander("Technical details"):
                        st.code(str(error))

    if st.session_state.analysis_result:
        st.markdown(
            """
            <div class="report-topline">
                <span class="report-label">✓ REPORT GENERATED</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.container(key="report_card"):
            st.markdown(st.session_state.analysis_result)

        st.download_button(
            "Download report (.txt)",
            data=st.session_state.analysis_result,
            file_name="SMART_LEGAL_AI_Report.txt",
            mime="text/plain",
            use_container_width=True,
        )

    else:
        st.markdown(
            """
            <div class="empty-report">
                <div>
                    <div class="empty-report-icon">⚖️</div>
                    <div class="empty-report-title">
                        Your report will appear here
                    </div>
                    <div class="empty-report-text">
                        Upload a document on the left and select
                        <b>Analyse Document with AI</b>.
                        Your extracted details, potential risks,
                        suggestions, and summary will appear here.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )