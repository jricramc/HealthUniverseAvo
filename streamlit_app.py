import streamlit as st
import requests
import json

# API_BASE_URL = "http://127.0.0.1:8000"  # Change to your FastAPI URL if hosted
API_BASE_URL = "https://avocado-backend-dtfu.onrender.com"

def call_api(endpoint, payload):
    """ Helper function to call API and return response """
    response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload)
    return response.json()

st.title("Build your own AI Medical Knowledge Base")

# Endpoint to add text chunks
st.header("Add Text from")
text = st.text_area("Enter text:")
title = st.text_input("Enter title:")
link = st.text_input("Enter link to article:")
if st.button("Add Text to article"):
    response = call_api("add_pharma", {"text": text, "title": title, "link": link})
    st.write(response)

# Interaction with scoring endpoint
st.header("Test our Health Content AI ")
query = st.text_area("Enter question for Avocado Health:")

# endpoint_options = ["hello", "guardrails", "fertilitae"]
# endpoint = st.selectbox("Select your desired endpoint:", endpoint_options)

use_guardrails = st.checkbox("Use Guardrails")
endpoint = "guardrails" if use_guardrails else "fertilitae"


if st.button("Ask a question"):
    response = call_api(endpoint, {"Query": query})

    response_dict = json.loads(response)

    print('response:', response)

    result = response_dict.get("result")
    references = response_dict.get("references")

    print("response_dict:", response_dict)

    # Present the result
    if result:
        st.markdown(f"**Result:** {result}")
    else:
        st.markdown("No result found.")

    # Check if there are any references
    if references:
        # Present the references
        st.markdown("**References:**")
        for ref in references:
            title = ref.get('title', '')
            link = ref.get('link', '')
            if link:
                st.markdown(f"- [{title}]({link})")
            else:
                st.markdown(f"- {title}")
    else:
        st.markdown("No references found.")
# Additional examples for each endpoint
# You can replicate the above examples for other endpoints

# Remember to handle different types of responses if necessary
