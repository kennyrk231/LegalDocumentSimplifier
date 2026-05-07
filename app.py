import streamlit as st
from legal_simplifier import LegalSimplifier

st.set_page_config(layout="wide")
st.title("⚖️ Legal Simplifier PRO")

# Sidebar
st.sidebar.title("📤 Input")
input_type = st.sidebar.radio("Method:", ["📝 Text", "📄 PDF"])

simplifier = LegalSimplifier()
text = ""

if input_type == "📝 Text":
    text = st.text_area("Paste legal text:", height=200, 
        placeholder="WHEREAS Party A shall indemnify...")
elif input_type == "📄 PDF":
    uploaded_file = st.sidebar.file_uploader("Upload PDF:", type="pdf")
    if uploaded_file:
        pdf_path = f"temp_{uploaded_file.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        text = simplifier.from_pdf(pdf_path)
        if "Error" not in text:
            st.sidebar.success(f"✅ {len(text)} chars extracted")

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🚀 SIMPLIFY", type="primary", use_container_width=True) and text.strip():
        orig_stats = simplifier.analyze(text)
        simplified = simplifier.simplify(text)
        simp_stats = simplifier.analyze(simplified)
        
        # Results
        st.subheader("📊 Before & After")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.metric("Original", f"Grade {orig_stats['grade_level']}")
            st.text_area("Original", text[:800], height=200)
        
        with col_b:
            reduction = (1 - simp_stats['words']/orig_stats['words']) * 100
            st.metric("Simplified", f"Grade {simp_stats['grade_level']}", f"{reduction:.0f}% shorter")
            st.text_area("Simplified", simplified, height=200)
        
        st.download_button("💾 Download", simplified, "simplified.txt")

if not text.strip():
    st.info("👈 Enter text or upload PDF")