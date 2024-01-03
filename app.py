import streamlit as st
import datetime
import json
import base64

# Function to save user data to a JSON file
def save_user_data(user_data_list, file_name="user_data.json"):
    json_file_path = file_name
    with open(json_file_path, "w") as json_file:
        json.dump(user_data_list, json_file, indent=4)

# Function to generate a download link for the JSON data
def get_table_download_link(json_data, file_name="user_data.json"):
    val = json.dumps(json_data, indent=4)
    b64 = base64.b64encode(val.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download JSON File</a>'
    return href

# Function to load user data from a JSON file
def load_user_data(file_name="user_data.json"):
    json_file_path = file_name
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
    height = st.number_input("Your Height", value=0, placeholder="Enter Your Height in feet ")
    yourinterests = st.text_input("Your Interests", placeholder="Music type, Dance, Sports and etc")

    user_data = {
        "name": name,
        "firstname": firstname,
        "secondname": secondname,
        "birthdate": str(birthdate) if birthdate else "", 
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

        # Submit button for user data
        if all_fields_filled and st.button("Submit User Data"):
            user_data_list.append(user_data)
            save_user_data(user_data_list)
            st.success("User data submitted successfully!")

    # Date's information form
    with st.form("date_info_form"):
        st.title("Date's Information")
        date_gender = st.text_input("Date's Gender", placeholder="Enter date's gender")
        date_religion = st.text_input("Date's faith community", placeholder="Enter date's religion / No religion")
        date_job = st.text_input("Date's position of employment", placeholder="Job / Student / other")
        high_preference = st.text_input("High Preference", placeholder="Date's gender & religion / gender & job / All")

        # Check if all required fields in the date form are filled
        all_date_fields_filled = all([date_gender, date_religion, date_job, high_preference])

        # Submit button for the date's form, enabled only when all fields are filled
        submit_date_info = st.form_submit_button("Submit Date's Information", disabled=not all_date_fields_filled)

    if submit_date_info:
        # Process and save date's information
        st.success("Date's information submitted successfully!")

        # Load date's data from JSON file
        dates_data_list = load_user_data("dates_data.json")
        date_info = {
            "date_gender": date_gender,
            "date_religion": date_religion,
            "date_job": date_job,
            "high_preference": high_preference
        }
        dates_data_list.append(date_info)
        save_user_data(dates_data_list, "dates_data.json")

        # Load user data again (in case new data was added)
        user_data_list = load_user_data()

        # Check preferences and find matching profiles
        matching_profiles = []
        for user in user_data_list:
            if high_preference == "Date's gender & religion" and user['gender'] == date_gender and user['religion'] == date_religion:
                matching_profiles.append(user)
            elif high_preference == "gender & job" and user['gender'] == date_gender and user['job'] == date_job:
                matching_profiles.append(user)
            elif high_preference == "All" and user['gender'] == date_gender and user['religion'] == date_religion and user['job'] == date_job:
                matching_profiles.append(user)

        # Display matching profiles
        if matching_profiles:
            for profile in matching_profiles:
                st.subheader(f"{profile['name']} - {profile['job']}")
                st.write(f"Religion: {profile['religion']}")
                st.write(f"Interests: {profile['interests']}")
                if 'image' in profile:
                    st.image(base64.b64decode(profile['image']), caption=profile['name'], use_column_width=True)
        else:
            st.write("No matching profiles found.")

    # Download button for user JSON data
    if st.button('Download User Data JSON'):
        user_data_list = load_user_data()
        st.markdown(get_table_download_link(user_data_list), unsafe_allow_html=True)

    # Download button for dates JSON data
    if st.button('Download Dates Data JSON'):
        dates_data_list = load_user_data("dates_data.json")
        st.markdown(get_table_download_link(dates_data_list, "dates_data.json"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
