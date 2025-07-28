import streamlit as st
from smtp_sendmail import sendEmail

st.set_page_config(page_title="Send Email", layout="wide")

st.title("Send Your Cold Email")

# Check session state
if "generated_email" not in st.session_state:
    st.warning("No email found. Please go back and generate one.")
    st.page_link("app/main.py", label="Back to Main")
    st.stop()

# Show email
st.subheader("Preview Email")
st.code(st.session_state.generated_email, language="markdown")

# Email form
st.subheader("Send Email")

sender = st.text_input("Your Gmail Address")
app_password = st.text_input("App Password (16 characters)", type="password")
receiver = st.text_input("Receiver's Email")
subject = st.text_input("Subject", value = st.session_state.subject if "subject" in st.session_state else "")

if st.button("Send Email"):
    if sender and app_password and receiver:
        result = sendEmail(sender, app_password, receiver, subject, st.session_state.generated_email)
        st.success(result) if "successfully" in result else st.error(result)
    else:
        st.warning("Please fill all the fields.")
