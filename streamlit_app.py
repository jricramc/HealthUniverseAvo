import streamlit as st
import requests
import json

API_BASE_URL = "https://avocado-backend-dtfu.onrender.com"

def call_api(endpoint, payload):
    """ Helper function to call API and return response """
    response = requests.post(f"{API_BASE_URL}/{endpoint}", json=payload)
    return response.json()

# Set the sidebar color and other styles
def set_custom_styles():
    st.markdown("""
    <style>
    .css-1d391kg {
        background-color: #2ca02c; /* Adjust the color to your preference */
        color: white;
    }
    .css-1aumxhk {
        background-color: #2ca02c;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

set_custom_styles()

# Initialize the session state for navigation if it doesn't exist
if 'navigation' not in st.session_state:
    st.session_state['navigation'] = 'learn_more'  # Set default to "learn_more" section

st.title("Avocado Health AI 🥑")

# Sidebar with navigation
st.sidebar.title("Navigation")
st.sidebar.header("Sections")

# Navigation links in the sidebar
if st.sidebar.button("Our technology"):
    st.session_state['navigation'] = 'learn_more'
if st.sidebar.button("Talk to your Knowledge Base"):
    st.session_state['navigation'] = 'test'
if st.sidebar.button("Build your Knowledge Base"):
    st.session_state['navigation'] = 'build'

# Sidebar about the app
st.sidebar.title("About This App")
st.sidebar.info(
    """
    This app allows you to build safe and hallucination-free AI chatbots for healthcare.
    """
)

# Display sections based on navigation state
if st.session_state['navigation'] == 'build':
    st.header("Add Text")
    text = st.text_area("Enter text:")
    title = st.text_input("Enter title:")
    link = st.text_input("Enter link to source:")
    if st.button("Add Text to Knowledge Base"):
        response = call_api("add_pharma", {"text": text, "title": title, "link": link})
        st.write(response)

elif st.session_state['navigation'] == 'learn_more':
    st.header("Welcome to Avocado Health AI")
    st.markdown(
        """
        Detailed information about how Avocado Health AI processes and understands medical content, including:
        - Data privacy
        - AI model training
        - Real-world applications
        """
       """
        Use Cases:
        - Patient education
        - Healthcare professional support
        """
    )

else:  # Default section "Test our Health Content AI"
    st.header("Ask a question")
    query = st.text_area("Enter question for Avocado Health:")
    use_guardrails = st.checkbox("Use Guardrails")
    endpoint = "guardrails" if use_guardrails else "fertilitae"

    if st.button("Submit"):
        response = call_api(endpoint, {"Query": query})
        response_dict = json.loads(response)

        result = response_dict.get("result")
        references = response_dict.get("references")

        if result:
            st.markdown(f"**Result:** {result}")
        else:
            st.markdown("No result found.")

        if references:
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
