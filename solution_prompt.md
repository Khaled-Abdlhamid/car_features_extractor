## Solution Prompt

i'm working on a pipeline that accepts a car image and description from a user and then passes the image for a model that classify the image to different body types and extracts a JSON from the description, and then the system sends the JSON and the image to a designated Gmail account.
here is what i want you to implement:  
1- a simple streamlit app that accepts the image and text description from the user.  
2- a python module that parses the text and uses GPT-4o-mini to extract the data in the following JSON format

'''
{
  "car": {
    "body_type": "string",
    "color": "string",
    "brand": "string",
    "model": "string",
    "manufactured_year": "integer",
    "motor_size_cc": "integer",
    "tires": {
      "type": "string",
      "manufactured_year": "integer"
    },
    "windows": "string",
    "notices": [
      {
        "type": "string",
        "description": "string"
      }
    ],
    "price": {
      "amount": "number",
      "currency": "string"
    }
  }
}
'''  
3- a python module that takes the output JSON and the image and sends them to a certain gmail address.
