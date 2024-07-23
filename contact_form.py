import streamlit as st
import streamlit.components.v1 as components

def contact():
  st.title('📨 Contact Form')
  
  st.markdown("##### If you have any questions, feedback, or encounter any issues using this app, please fill out "
                  "the form below, and I'll get back to you as soon as possible.")
  
  # Embed the Google Form using an iframe
  components.html(
      f"""
  <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScLaMWyScjbqoo6I5w5MtoQwfSU-Izghn1y_jsTP-yuf5zZOA/viewform?embedded=true" width="640" height="741" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
      
      """,
      height=1800,
  )




