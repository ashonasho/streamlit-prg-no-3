import streamlit as st 
import datetime
import json
import base64
import os

def main():
    st.title("Let's Date")
    st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

    name = st.text_input("Your name", placeholder="short name / your name")
    st.write("Welcome", name)

    firstname = st.text_input("Firstname", placeholder="Enter your first name")
    secondname = st.text_input("Secondname", placeholder="Enter your second name / No second name")
    birthdate = st.date_input("Birth Date", format="DD.MM.YYYY")
    religion = st.text_input("Faith community", placeholder="Enter your religion / No religion")
    job = st.text_input("Position of employment", placeholder="Job / Student / other")
    gender = st.radio("Your Gender", ["Male", "Female", "Other"])
    height = st.number_input("Your Height", value=None, placeholder="Enter Your Height in feet ")
    yourinterests = st.text_input("Your Interests", placeholder="Music type, Dance, Sports and etc")

    user_data = {
        "name": name,
        "firstname": firstname,
        "secondname": secondname,
        "birthdate": str(birthdate) if birthdate is not None else None, 
        "religion": religion,
        "job": job,
        "gender": gender,
        "height": height,
        "interests": yourinterests
    }

    st.title("Please upload your image.")

    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")

        # Check if all required fields are filled
        all_fields_filled = all(value is not None and (isinstance(value, str) and value.strip() or True) for value in user_data.values())

        # Show the submit button only when all requirements are filled
        if all_fields_filled and st.button("Submit"):
            json_file_path = "user_data.json"
            # Save the uploaded file with a unique name
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
            file_name = os.path.join("uploads", uploaded_file.name)
            with open(file_name, "wb") as file:
                file.write(uploaded_file.read())
            user_data["image"] = file_name

            # Convert the user data to JSON
            user_json = json.dumps(user_data, indent=4)

            # Save the JSON data to a file
            with open(json_file_path, "w") as json_file:
                json_file.write(user_json)

            st.success("User data submitted successfully!")

if __name__ == "__main__":
    main()
