import streamlit as st
from datetime import datetime
from text_extractor import extract_listing
from car_type_classifier import classify_car_type
from gmail_sender import send_email_with_json_and_image   # <-- import your email sender
import json
import asyncio
import os

st.set_page_config(page_title="Car Listing Extractor", page_icon="🚗", layout="centered")
st.title("🚗 Car Listing Extractor (MVP)")
st.caption("Upload a car image + paste a description. We extract structured JSON from text and add car_type from a dummy classifier.")

# ---- Inputs
img_file = st.file_uploader("Car image", type=["jpg","jpeg","png"])
desc = st.text_area("Car description", height=180, placeholder="e.g., 2018 Toyota Corolla, white, 75k km, automatic ...")

submit_btn = st.button("✅ Extract JSON", type="primary", use_container_width=True)
send_btn = st.button("📧 Send to Gmail", type="secondary", use_container_width=True)

# ---- State
if "listing" not in st.session_state:
    st.session_state["listing"] = None
if "image_path" not in st.session_state:
    st.session_state["image_path"] = None


def run_extraction():
    """Run extraction and classification"""
    if not img_file:
        st.error("Please upload an image.")
        return
    if not desc.strip():
        st.error("Please enter a description.")
        return

    # ---- 1. Extract JSON from description
    listing = asyncio.run(extract_listing(desc))

    # ---- 2. Dummy car type classification
    car_type = classify_car_type(img_file)

    # ---- 3. Merge results (update inside car object)
    if "car" in listing and isinstance(listing["car"], dict):
        listing["car"]["body_type"] = car_type

    # Save image temporarily to disk for email sending
    image_path = f"temp_{img_file.name}"
    with open(image_path, "wb") as f:
        f.write(img_file.getbuffer())

    # Save to session state
    st.session_state["listing"] = listing
    st.session_state["image_path"] = image_path

    # ---- 4. Display final result
    st.subheader("Extracted JSON + Car Type")
    st.code(json.dumps(listing, indent=2), language="json") 
    st.success("Extraction complete! You can now send this data via Gmail.")


def run_sender():
    """Send JSON + uploaded image to Gmail"""
    if not st.session_state["listing"]:
        st.error("No extracted listing found. Please extract JSON first.")
        return
    if not st.session_state["image_path"]:
        st.error("No image found. Please re-upload and extract first.")
        return

    try:
        sender_email = ""
        sender_password = "" 
        recipient_email = ""
        subject = "Car Listing Extracted Data"
        body = json.dumps(st.session_state["listing"], indent=2)

        send_email_with_json_and_image(sender_email=sender_email, 
                                       sender_password=sender_password, 
                                       recipient_email=recipient_email, 
                                       extracted_json=body,
                                       image_path= st.session_state["image_path"])

        st.success(f"✅ Email sent successfully to {recipient_email}!")

    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")


# ---- Button logic
if submit_btn:
    run_extraction()

if send_btn:
    run_sender()
