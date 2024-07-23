# import streamlit as st
# import requests

import streamlit as st
import streamlit.components.v1 as components

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


# # Function to apply custom CSS styling
# def apply_custom_css():
#     st.markdown(
#         """
#         <style>
#         body {font-family: Arial, Helvetica, sans-serif;}
#         * {box-sizing: border-box;}

#         input[type=text], select, textarea {
#           width: 100%;
#           padding: 12px;
#           border: 1px solid #ccc;
#           border-radius: 4px;
#           box-sizing: border-box;
#           margin-top: 6px;
#           margin-bottom: 16px;
#           resize: vertical;
#         }
#         input[type=email], select, textarea {
#           width: 100%;
#           padding: 12px;
#           border: 1px solid #ccc;
#           border-radius: 4px;
#           box-sizing: border-box;
#           margin-top: 6px;
#           margin-bottom: 16px;
#           resize: vertical;
#         }

#         input[type=submit] {
#           background-color: #04AA6D;
#           color: white;
#           padding: 12px 20px;
#           border: none;
#           border-radius: 4px;
#           cursor: pointer;
#         }

#         input[type=submit]:hover {
#           background-color: #45a049;
#         }

#         .container {
#           border-radius: 5px;
#           background-color: #f2f2f2;
#           padding: 20px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
# def contact():
#     st.subheader("📨 Contact Form")
#     st.markdown("##### If you have any questions, feedback, or encounter any issues using this app, please fill out "
#                 "the form below, and I'll get back to you as soon as possible.")
#     apply_custom_css()
#     contact_form = """
#             <div class="container">
#                 <form action="https://formsubmit.co/d68136092d5b1774aa904c6fd1a654aa" method="POST">
#                     <label for="name">Name</label>
#                     <input type="text" name="name" placeholder="Your name.." required>
#                     <label for="email">Email</label>
#                     <input type="email" id="email" name="email" placeholder="Your email.." required>
#                     <label for="subject">Subject</label>
#                     <textarea id="subject" name="subject" placeholder="Your message.." required style="height:200px"></textarea>
#                     <input type="submit" value="Submit">
#                 </form>
#             </div>
#                 """

#     st.markdown(contact_form, unsafe_allow_html=True)

