import streamlit as st
from datetime import datetime
from text_extractor import extract_listing
from car_type_classifier import classify_car_type
import json
import asyncio

st.set_page_config(page_title="Car Listing Extractor", page_icon="🚗", layout="centered")
st.title("🚗 Car Listing Extractor (MVP)")
st.caption("Upload a car image + paste a description. We extract structured JSON from text and add car_type from a dummy classifier.")

# ---- Inputs
img_file = st.file_uploader("Car image", type=["jpg","jpeg","png"])
desc = st.text_area("Car description", height=180, placeholder="e.g., 2018 Toyota Corolla, white, 75k km, automatic ...")
submit_btn = st.button("✅ Submit", type="primary", use_container_width=True)


def run(generate: bool):
    if not img_file:
        st.error("Please upload an image.")
        return
    if not desc.strip():
        st.error("Please enter a description.")
        return

    listing = asyncio.run(extract_listing(desc))
    
    st.subheader("Extracted JSON")
    # st.code(listing.model_dump_json(indent=2), language="json")
    st.code(json.dumps(listing, indent=2), language="json") 
    st.info("Email integration will be added next. For now, verify the JSON looks right.")

if submit_btn:
    run(generate=True)
