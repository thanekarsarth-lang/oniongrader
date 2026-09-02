import streamlit as st
from PIL import Image
from predict import predict

st.set_page_config(
    page_title="OnionAI",
    page_icon="🧅",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f6f1;
}

.block-container {
    max-width: 1200px;
    padding: 30px 40px 50px;
}

.header {
    background: #17251b;
    padding: 38px 45px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;
}

.header-small {
    color: #a9c5a7;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}

.header-title {
    font-size: 46px;
    font-weight: 800;
    margin: 8px 0;
}

.header-text {
    color: #c9d6c8;
    font-size: 17px;
}

.info-card {
    background: white;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid #e1e6dd;
    min-height: 145px;
}

.info-icon {
    font-size: 30px;
}

.info-title {
    font-size: 17px;
    font-weight: 700;
    margin-top: 10px;
}

.info-text {
    color: #747b73;
    font-size: 14px;
}

.card {
    background: white;
    padding: 28px;
    border-radius: 22px;
    border: 1px solid #e1e6dd;
    margin-top: 25px;
}

.section-title {
    font-size: 22px;
    font-weight: 800;
    color: #17251b;
}

.section-subtitle {
    color: #777e75;
    font-size: 14px;
    margin-bottom: 20px;
}

.result-good {
    background: #eaf7ed;
    border: 2px solid #91c89b;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    margin-top: 15px;
}

.result-bad {
    background: #fff0ef;
    border: 2px solid #e0a09a;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    margin-top: 15px;
}

.result-icon {
    font-size: 48px;
}

.result-title {
    font-size: 29px;
    font-weight: 800;
    margin-top: 8px;
}

.result-description {
    color: #656b64;
    margin-top: 5px;
}

.metric-box {
    background: #f7f9f5;
    padding: 20px;
    border-radius: 18px;
    text-align: center;
    margin-top: 18px;
}

.metric-number {
    font-size: 32px;
    font-weight: 800;
    color: #17251b;
}

.metric-label {
    color: #777e75;
    font-size: 13px;
    font-weight: 600;
}

.footer {
    text-align: center;
    color: #8a9187;
    font-size: 13px;
    margin-top: 40px;
}

div.stButton > button {
    border-radius: 14px;
    height: 52px;
    font-size: 16px;
    font-weight: 700;
}

[data-testid="stFileUploader"] {
    background: #f8faf6;
    border: 2px dashed #aebbaa;
    border-radius: 18px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">
    <div class="header-small">AI AGRICULTURE • QUALITY INSPECTION</div>
    <div class="header-title">🧅 OnionAI</div>
    <div class="header-text">
        Intelligent visual grading for faster and smarter onion procurement.
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">📷</div>
        <div class="info-title">Visual Inspection</div>
        <div class="info-text">
            Upload an onion image for automated visual assessment.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🧠</div>
        <div class="info-title">AI Analysis</div>
        <div class="info-text">
            Our trained model analyzes the visual quality of the onion.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">📦</div>
        <div class="info-title">Procurement Decision</div>
        <div class="info-text">
            Get an instant recommendation for procurement.
        </div>
    </div>
    """, unsafe_allow_html=True)

left, right = st.columns([1, 1], gap="large")

with left:

    st.markdown("""
    <div class="card">
        <div class="section-title">📤 Upload Onion</div>
        <div class="section-subtitle">
            Upload a clear image of an onion.
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        st.image(
            image,
            caption="Uploaded Onion",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

with right:

    st.markdown("""
    <div class="card">
        <div class="section-title">🔬 Quality Assessment</div>
        <div class="section-subtitle">
            Let AI evaluate the uploaded onion.
        </div>
    """, unsafe_allow_html=True)

    if uploaded_file is None:

        st.markdown("""
        <div style="
            background:#f7f9f5;
            border-radius:18px;
            padding:65px 20px;
            text-align:center;
            border:1px solid #e4e9e0;
        ">
            <div style="font-size:55px;">🧅</div>
            <h3>Ready for inspection</h3>
            <p style="color:#777e75;">
                Upload an onion image to begin.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:

        if st.button(
            "🔍  ANALYZE ONION",
            use_container_width=True
        ):

            with st.spinner("Analyzing onion quality..."):

                label, confidence = predict(image)

            if label == "good":

                st.markdown("""
                <div class="result-good">
                    <div class="result-icon">🟢</div>
                    <div class="result-title">GOOD QUALITY</div>
                    <div class="result-description">
                        Onion appears suitable for procurement.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.success("✅ Recommended for procurement")

            else:

                st.markdown("""
                <div class="result-bad">
                    <div class="result-icon">🔴</div>
                    <div class="result-title">LOWER QUALITY</div>
                    <div class="result-description">
                        Onion requires rejection or manual inspection.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.warning("⚠️ Reject or send for manual inspection")

            st.markdown(f"""
            <div class="metric-box">
                <div class="metric-number">{confidence:.1f}%</div>
                <div class="metric-label">AI CONFIDENCE</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    OnionAI • AI-Assisted Agricultural Quality Grading • Hackathon MVP
</div>
""", unsafe_allow_html=True)