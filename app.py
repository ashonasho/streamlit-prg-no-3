import streamlit as st 
import datetime


st.title("Let's Date")
st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

name = st.text_input("Yourname", placeholder="short name/your name")
st.write("Welcome", name)

firstname = st.text_input("Firstname", placeholder="Enter your first name")
secondname = st.text_input("Secondname", placeholder="Enter your second name")
birthdate= st.date_input("Birth Date", format="DD.MM.YYYY", placeholder="DD.MM.YYYY")