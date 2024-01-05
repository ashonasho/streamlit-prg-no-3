import streamlit as st
import datetime
import json
import base64
import openai

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"  # Replace with your actual OpenAI API key

def save_user_data(user_data_list, file_name="user_data.json"):
    with open(file_name, "w") as json_file:
        json.dump(user_data_list, json_file, indent=4)

def get_table_download_link(json_data, file_name="user_data.json"):
    val = json.dumps(json_data, indent=4)
    b64 = base64.b64encode(val.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download JSON File</a>'
    return href

def load_user_data(file_name="user_data.json"):
    try:
        with open(file_name, "r") as json_file:
            user_data_list = json.load(json_file)
    except FileNotFoundError:
        st.error(f"File not found: {file_name}")
        user_data_list = []
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from file: {file_name}")
        user_data_list = []
    except Exception as e:
        st.error(f"An error occurred: {e}")
        user_data_list = []
    return user_data_list

def load_user_data_without_image(file_name="user_data.json"):
    user_data_list = load_user_data(file_name)
    for user_data in user_data_list:
        user_data.pop("image", None)  # Remove image data
    return user_data_list

def call_gpt3_match_finding(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def main():
    st.title("Let's Date")
    st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

    user_data_list = load_user_data_without_image()  # Loading data without images

    # User Input Fields
    name = st.text_input("Your name", placeholder="Short name / Your name")
    st.write("Welcome", name)
    firstname = st.text_input("Firstname", placeholder="Enter your first name")
    secondname = st.text_input("Secondname", placeholder="Enter your second name / No second name")
    birthdate = st.date_input("Birth Date")
    religion = st.selectbox("Religion", options=["Hindu", "Rc", "Non Rc", "Muslim", "Buddhism"], key="religion")
    job = st.selectbox("Position of employment", options=["Doctor", "Engineer", "Nurse", "Software Engineer", "Teacher", "App developer", "Farmer", "Businessman", "Software Developer", "Coach", "Qs", "Architect", "Banker", "District coordinator", "TL", "HR", "Dentist", "Manager", "Waiter", "Technicians", "Scientist", "Care aker", "Barber", "AI developer", "Tailor", "Delivery service", "House Cleaner", "Driver", "Attendant", "Part-timer", "Student", "Actor", "Other", "No job"], key="job")
    gender = st.radio("Your Gender", ["Male", "Female", "Other"])
    height = st.number_input("Your Height", min_value=0.0, max_value=10.0, step=0.1, format="%.1f")
    yourinterests = st.text_input("Your Interests", placeholder="Music type, Dance, Sports etc.")

    # Image Upload
    uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")
        user_data = {
            "name": name,
            "firstname": firstname,
            "secondname": secondname,
            "birthdate": str(birthdate) if birthdate else "",
            "religion": religion,
            "job": job,
            "gender": gender,
            "height": height,
            "interests": yourinterests,
            "image": image_data
        }
        all_fields_filled = all(value for value in user_data.values() if isinstance(value, str))
        if all_fields_filled and st.button("Submit User Data"):
            user_data_list.append(user_data)
            save_user_data(user_data_list)
            st.success("User data submitted successfully!")

    # Date's Information Form
    with st.form("date_info_form"):
        date_gender = st.radio("Date's Gender", ["Male", "Female", "Other"], key="date_gender")
        date_religion = st.selectbox("Date's Religion", options=["Hindu", "Rc", "Non Rc", "Muslim", "Buddhism"], key="date_religion")
        date_job = st.selectbox("Date's Job", options=["Doctor", "Engineer", "Nurse", "Software Engineer", "Teacher", "App developer", "Farmer", "Businessman", "Software Developer", "Coach", "Qs", "Architect", "Banker", "District coordinator", "TL", "HR", "Dentist", "Manager", "Waiter", "Technicians", "Scientist", "Care aker", "Barber", "AI developer", "Tailor", "Delivery service", "House Cleaner", "Driver", "Attendant", "Part-timer", "Student", "Actor", "Other", "No job"], key="date_job")
        high_preference = st.selectbox("High Preference", options=["gender & religion", "gender & job", "All"], key="high_preference")
        submit_date_info = st.form_submit_button("Submit Date's Information")

    if submit_date_info:
        match_finding_prompt = f"Find a match for a {date_gender} of {date_religion} religion and {date_job} job with high preference for {high_preference}"
        match_result = call_gpt3_match_finding(match_finding_prompt)
        st.success("Date's information submitted successfully!")
        # Matching logic based on the user's preferences
        # ...

    # Download Buttons for User Data and Dates Data
    if st.button('Download User Data JSON'):
        user_data_list = load_user_data_without_image()
        st.markdown(get_table_download_link(user_data_list), unsafe_allow_html=True)

    if st.button('Download Dates Data JSON'):
        dates_data_list = load_user_data_without_image("dates_data.json")
        st.markdown(get_table_download_link(dates_data_list, "dates_data.json"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
