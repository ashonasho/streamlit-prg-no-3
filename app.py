import streamlit as st 
import datetime


st.title("Let's Date")
st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

name = st.text_input("Yourname", placeholder="short name / your name")
st.write("Welcome", name)

firstname = st.text_input("Firstname", placeholder="Enter your first name")
secondname = st.text_input("Secondname", placeholder="Enter your second name / No second name")
birthdate= st.date_input("Birth Date", format="DD.MM.YYYY")
religion = st.text_input("faith community", placeholder="Enter your religion / No religion")
job = st.text_input("position of employment", placeholder="Job / Student / other")
gender = st.radio("Your Gender", ["Male", "Female"])
heigth = st.number_input("Your Height", value=None, placeholder="Enter Your Height in feet ")
yourinterests = st.text_input("Your Interests", placeholder="Music type,Dance,Sports and etc")



def main():
    
    st.title("Please upload your image.")

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying... (add your image processing logic here)")

if __name__ == "__main__":
    main()

st.button("submit")
