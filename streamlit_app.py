import streamlit as st
import requests
import json

API_BASE_URL = "https://avocado-backend-dtfu.onrender.com"
# API_BASE_URL = "http://127.0.0.1:8000"


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

st.markdown("""
<div style="background-color: #f4f4f5; padding: 10px; border-radius: 5px; border: 1px solid #ccc;">
    <b>Disclaimer:</b> This application is a demo and for educational purposes only. It is not intended to replace professional medical advice or treatment.
</div>
""", unsafe_allow_html=True)

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
if st.sidebar.button("Demo"):  # New button for Zocalo Demo
    st.session_state['navigation'] = 'demo'

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
        Avocado is a low hallucination AI pipeline designed to enhance health applications by incorporating a safety layer atop existing AI models. This integration significantly reduces hallucinations, facilitating the safe and reliable generation of health content. Health organizations can utilize their compiled knowledge bases—including articles, reports, and other resources—to create AI-driven chatbots that deliver accurate and personalized health information.

        Whether you are a healthcare provider, a pharma company, or a wellness organization, Avocado Health AI can help you deliver personalized and engaging health content to your users. Try it out and see the power of AI in healthcare!
        """
       """
        Use Cases:
        - Patient Education/Guidance: Imagine a scenario where a patient needs to understand their new diabetes medication regimen. Avocado can converse with the patient, explaining the timing, dosage, and side effects, thus reducing the workload on healthcare professionals.
        - Drug Information: Pharma companies can use Avocado to inform both consumers and clinicians about drug interactions, benefits, and clinical study findings.
        - Personalized Health Risk Assessments: Avocado can be utilized by healthcare providers or wellness companies to offer personalized health risk assessments. Users can input their medical history, lifestyle choices, family health history, and other relevant information. The AI then analyzes this data against a broad knowledge base to identify potential health risks and provide personalized preventive health advice.
        """
        """
        Limitations:
        - Avocado is not a replacement for professional medical advice. Always consult a healthcare professional for medical advice and treatment.
        - Avocado is not a diagnostic tool. It is designed to provide general health information and guidance.
        - Avocado is not a substitute for human interaction
        """
        
    )

elif st.session_state['navigation'] == 'demo':  # New section for Zocalo Demo
    st.header("Enter your symptoms")
    symptoms = st.text_input("Tell us how you have felt: enter your symptoms")

    if symptoms:
        st.header("Follow-up question")
        follow_up = st.text_input("How long have you been feeling this way and what medicine have you taken so far?")
        
        if st.button("Submit"):
            response = call_api("symptom_check", {"symptoms": symptoms, "feeling_and_medicine": follow_up})
            st.write(response)

        print("followup", follow_up)
    print("symptoms", symptoms)



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
