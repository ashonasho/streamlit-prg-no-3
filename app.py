import streamlit as st
import datetime
import json
import base64

# Function to save user data to a JSON file
def save_user_data(user_data_list):
    json_file_path = "user_data.json"
    with open(json_file_path, "w") as json_file:
        json.dump(user_data_list, json_file, indent=4)

# Function to generate a download link for the JSON data
def get_table_download_link(json_data):
    val = json.dumps(json_data, indent=4)
    b64 = base64.b64encode(val.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="user_data.json">Download JSON File</a>'
    return href

# Function to load user data from a JSON file
def load_user_data():
    json_file_path = "user_data.json"
    try:
        with open(json_file_path, "r") as json_file:
            user_data_list = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data_list = []
    return user_data_list

def main():
    st.title("Let's Date")
    st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

    user_data_list = load_user_data()

    # User input fields
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

    # Initialize a flag for successful submission
    data_submitted = False

    # Check if all required fields and image are filled
    all_fields_filled = all(value is not None and (isinstance(value, str) and value.strip() or True) for value in user_data.values())

    # Show the submit button only when all requirements are filled
    if all_fields_filled and st.button("Submit"):
        user_data_list.append(user_data)
        
        # Save the updated user data to the JSON file
        save_user_data(user_data_list)

        st.success("User data submitted successfully!")
        data_submitted = True  # Update the flag after successful submission

    # Display the download link only after successful submission
    if data_submitted:
        st.markdown(get_table_download_link(user_data_list), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
