# Car features Extractor (Assessment Project)

### Overview
This application allows users to list cars on an online platform by uploading:
- A car image
- A text description
The app extracts structured JSON data from the description, identifies the car type (dummy classifier for now), and sends both the JSON + image to a designated Gmail inbox.

### Key Features
- GUI for image + text input.
- Text → JSON conversion using GPT-4o-mini.
- Prompt injection safeguards to prevent malicious misuse.
- Dummy car type classifier (simulates real CV model integration).
- Email sender (sends structured JSON + image to Gmail).

### Setup Instructions
1- Clone the Repository  
2- Create a Virtual Environment  
3- Install Dependencies: pip install -r requirements.txt  
4- Configure Environment Variables: Copy .env.example → .env and update values  
5- Run the Application: streamlit run ui_app.py

### Usage Guide
1- Upload Car Image.
2- Paste Car Description.
3- Click "Extract JSON" or "Send to Gmail"

### Solution Design
see solution_design.png

### Solution Creation Prompt
see solution_prompt.md
