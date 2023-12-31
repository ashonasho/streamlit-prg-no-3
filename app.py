import streamlit as st 
import datetime
import json
import base64

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
height = st.number_input("Your Height", value=None, placeholder="Enter Your Height in feet ")
yourinterests = st.text_input("Your Interests", placeholder="Music type,Dance,Sports and etc")


user_data = {
    "name": name,
    "firstname": firstname,
    "secondname": secondname,
    "birthdate": str(birthdate),
    "religion": religion,
    "job": job,
    "gender": gender,
    "height": height,
    "interests": yourinterests
}


def main():
    
    st.title("Please upload your image.")

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:

        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying... (add your image processing logic here)")

        user_data["image"] = image_data



if st.button("Submit"):
    
    if all(value and value.strip() for value in user_data.values()):
        json_file_path = "user_data.json"

        user_json = json.dumps(user_data, indent=4)

        
        with open(json_file_path, "w") as json_file:
            json_file.write(user_json)

        st.success("User data submitted successfully!")
    else:
        st.warning("Please fill in all the required fields and upload an image.")

if __name__ == "__main__":
    main()
