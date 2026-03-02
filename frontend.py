import streamlit as st
import requests

st.set_page_config(page_title="SHL AI Assessment Recommender", layout="centered")

st.title("🔍 SHL AI Assessment Recommender")

st.markdown("""
This AI-powered system recommends relevant SHL assessments 
based on job descriptions using semantic search.

Simply paste the job description below and get intelligent recommendations.
""")

query = st.text_area("Enter Job Description", height=200)

top_k = st.slider("Number of Recommendations", min_value=5, max_value=20, value=10)

if st.button("Get Recommendations"):
    if query.strip():
        response = requests.post(
            "http://127.0.0.1:8000/recommend",
            json={"query": query, "top_k": top_k}
        )

        if response.status_code == 200:
            results = response.json()["recommended_assessments"]

            for test in results:
                st.subheader(test["name"])
                st.write("URL:", test["url"])
                st.write("Description:", test["description"])
                st.write("Duration:", test["duration"], "minutes")
                st.write("Test Type:", ", ".join(test["test_type"]))
                st.markdown("---")
        else:
            st.error("Error fetching recommendations.")
    else:
        st.warning("Please enter a job description.")