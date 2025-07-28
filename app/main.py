import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio

def create_streamlit_app(llm, portfolio):
    st.title("Email Generator For Job Posting")
    user_name = st.text_input("Enter Your Full Name:")
    institution = st.text_input("Enter Your Institution:")
    batch = st.text_input("Enter Your Batch (e.g., 2024):")
    cgpa = st.text_input("Enter Your CGPA:")
    resume = st.text_input("Enter resume open-link:")
    url_input = st.text_input("Enter a URL of Job Posting:")

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = loader.load().pop().page_content
            portfolio.load_portfolio()
            job = llm.extract_jobs(data)
            skills = job[0].get('skills',[]) if job else []
            user_profile = {
                "name": user_name,
                "institution": institution,
                "batch": batch,
                "cgpa": cgpa,
                "resume": resume
            }
            email = llm.write_mail(job,user_profile = user_profile)

            # Save to session state
            st.session_state.generated_email = email

            # Redirect
            st.success("Email generated successfully. Proceed to send it.")
            st.page_link("pages/send_email.py", label="Go to Send Email Page")

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator")
    create_streamlit_app(chain, portfolio)
