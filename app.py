import streamlit as st 
import datetime
import json
import base64

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
        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")

        user_data["image"] = image_data

        # Check if all required fields and image are filled
        all_fields_filled = all(value is not None and (isinstance(value, str) and value.strip() or True) for value in user_data.values())

        # Show the submit button only when all requirements are filled
        if all_fields_filled and st.button("Submit"):
            json_file_path = "user_data.json"
            user_json = json.dumps(user_data, indent=4)

            with open(json_file_path, "w") as json_file:
                json_file.write(user_json)

            st.success("User data submitted successfully!")

            # After submitting user data, create a new page to ask for date's information
            st.title("Date's Information")

            # Create placeholders for user input
            date_gender_placeholder = st.empty()
            date_religion_placeholder = st.empty()
            date_job_placeholder = st.empty()
            high_preference_placeholder = st.empty()

            # Ask for date's information
            date_gender = date_gender_placeholder.text_input("Date's Gender", placeholder="Enter date's gender")
            date_religion = date_religion_placeholder.text_input("Date's faith community", placeholder="Enter date's religion / No religion")
            date_job = date_job_placeholder.text_input("Date's position of employment", placeholder="Job / Student / other")
            high_preference = high_preference_placeholder.text_input("High Preference", placeholder=" Date's gender & religion / gender & job/ All")

if __name__ == "__main__":
    main()
