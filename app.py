import streamlit as st 
import datetime
import json
import base64

# Define the JSON file path
json_file_path = "user_data.json"

# Try to load existing data, or create an empty list if the file doesn't exist
try:
    with open(json_file_path, "r") as json_file:
        user_data_list = json.load(json_file)
except (FileNotFoundError, json.JSONDecodeError):
    user_data_list = []

def main():
    global user_data_list  # Make user_data_list a global variable

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

    if all_fields_filled and st.button("Submit"):
        # Append the new user data to the list
        user_data_list.append(user_data)

        # Write the updated list back to the JSON file
        with open(json_file_path, "w") as file:
            json.dump(user_data_list, file, indent=4)

        st.success("User data submitted successfully!")

        # Display the newly added user data
        st.title("Newly Added User Data")
        st.json(user_data)

    # Code for Date's Information form here...

if __name__ == "__main__":
    main()
