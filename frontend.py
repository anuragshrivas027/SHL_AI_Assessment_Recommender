import streamlit as st
import requests

# 🔹 Replace with your actual Railway backend URL
API_URL = "https://shlaiassessmentrecommender-production.up.railway.app/recommend"

st.set_page_config(page_title="SHL AI Assessment Recommender", layout="centered")

st.title("🔍 SHL AI Assessment Recommender")

st.markdown("""
This AI-powered system recommends relevant SHL assessments 
based on job descriptions using semantic search.

Simply paste the job description below and get intelligent recommendations.
""")

query = st.text_area("Enter Job Description", height=200)

top_k = st.slider("Number of Recommendations", min_value=5, max_value=10, value=5)

if st.button("Get Recommendations"):
    if query.strip():
        try:
            response = requests.post(
                API_URL,
                json={"query": query, "top_k": top_k},
                timeout=60
            )

            if response.status_code == 200:
                st.write(response.json())
                results = response.json().get("recommended_assessments", [])

                if results:
                    for test in results:
                        st.subheader(test.get("name", "N/A"))
                        st.write("URL:", test.get("url", "N/A"))
                        st.write("Description:", test.get("description", "N/A"))
                        st.write("Duration:", test.get("duration", 0), "minutes")
                        st.write("Test Type:", ", ".join(test.get("test_type", [])))
                        st.write("Adaptive Support:", test.get("adaptive_support", "N/A"))
                        st.write("Remote Support:", test.get("remote_support", "N/A"))
                        st.markdown("---")
                else:
                    st.warning("No recommendations found.")
            else:
                st.error(f"API Error: {response.status_code}")
        
        except requests.exceptions.RequestException:
            st.error("Unable to connect to the recommendation service. Please try again later.")
    else:
        st.warning("Please enter a job description.")