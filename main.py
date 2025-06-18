import streamlit as st
from navigator_agent import run_navigation


st.set_page_config(page_title="AI Product Navigator", layout="centered")
st.title("🚀 AI Web Navigator for Bunnings")

product_name = st.text_input("Enter the product to search on Bunnings:", "hammer")

if st.button("Start Navigation"):
    with st.spinner("Navigating website using AI agent..."):
        print("Running navigator")
        result = run_navigation(product_name)
    st.success("Done!")
    st.write(result)
