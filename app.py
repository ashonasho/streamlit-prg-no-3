import streamlit as st
import datetime
import json
import base64
import openai
from openai import OpenAI
import os

# Function to save user data to a JSON file
def save_user_data(user_data_list, file_name="user_data.json"):
    json_file_path = file_name
    try:
        with open(json_file_path, "w") as json_file:
            json.dump(user_data_list, json_file, indent=4)
        st.success(f"Data saved to {json_file_path}")  # Debug message
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Function to generate a download link for the JSON data
def get_table_download_link(json_data, file_name="user_data.json"):
    val = json.dumps(json_data, indent=4)
    b64 = base64.b64encode(val.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="{file_name}">Download JSON File</a>'
    return href

def load_user_data_without_image(file_name="user_data.json"):
    json_file_path = file_name
    try:
        with open(json_file_path, "r") as json_file:
            user_data_list = json.load(json_file)
            for user_data in user_data_list:
                user_data.pop("image", None)  # Remove image data
    except (FileNotFoundError, json.JSONDecodeError):
        user_data_list = []
    return user_data_list

# Function to call GPT-3.5 for match-finding prompts
def call_gpt3(prompt):
    openai.api_key = os.environ['OPENAI_API_KEY']  # Environment variable-l irunthu API key get pannuthu
    client = OpenAI()  # OpenAI client create pannuthu

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",  # GPT-3.5 model specify pannuthu
        prompt=prompt,  # User kudutha prompt pass pannuthu
        max_tokens = 1000  # Maximum number of tokens (words) specify pannuthu
    )
   
    return response.choices[0].text 

def main():
    st.title("Let's Date")
    st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

    user_data_list = load_user_data_without_image()

    # User input fields
    name = st.text_input("Your name", placeholder="short name / your name")
    st.write("Welcome", name)

    firstname = st.text_input("Firstname", placeholder="Enter your first name")
    secondname = st.text_input("Secondname", placeholder="Enter your second name / No second name")
    birthdate = st.date_input("Birth Date", format="DD.MM.YYYY")
    religion = st.selectbox("Religion", options=["Hindu","Rc","Non Rc","Muslim","Buddhism"], key="religion" )
    job = st.selectbox("Position of employment",options=["Doctor","Engineer","Nurse","Software Engineer","Teacher","App developer","Farmer","Businessman","Software Developer","Coach","Qs","Architect","Banker","District coordinator","TL","HR","Dentist","Manager","Waiter","Technicians","Scientist","Care aker","Barber","AI developer","Tailor","Delivery service","House Cleaner","Driver","Attendant","Part-timer","Student","actor","Other","No job"], key="job")
    gender = st.radio("Your Gender", ["Male", "Female", "Other"])
    height = st.number_input("Your Height", value=None, placeholder="Enter Your Height in feet ")
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

        all_fields_filled = all(value is not None and (isinstance(value, str) and value.strip() or True) for value in user_data.values())

        if all_fields_filled and st.button("Submit User Data"):
            user_data_list.append(user_data)
            save_user_data(user_data_list)
            st.success("User data submitted successfully!")

    with st.form("date_info_form"):
        st.title("Date's Information")
        date_gender = st.radio("Date's Gender", ["Male", "Female", "Other"], key="date_gender")
        date_religion = st.selectbox("Date's Religion", options=["Hindu","Rc","Non Rc","Muslim","Buddhism"], key="date_religion" )
        date_job = st.selectbox("Date's Job",options=["Doctor","Engineer","Nurse","Software Engineer","Teacher","App developer","Farmer","Businessman","Software Developer","Coach","Qs","Architect","Banker","District coordinator","TL","HR","Dentist","Manager","Waiter","Technicians","Scientist","Care aker","Barber","AI developer","Tailor","Delivery service","House Cleaner","Driver","Attendant","Part-timer","Student","actor","Other","No job"], key="date_job")
        high_preference = st.selectbox("High Preference", options=["gender & religion", "gender & job", "All"], key="high_preference")

        submit_date_info = st.form_submit_button("Submit Date's Information")

    if submit_date_info:
        match_finding_prompt = f"Find a match for a person with the following preferences: Gender - {date_gender}, Religion - {date_religion}, Job - {date_job}, The high preference is {high_preference}."

        user_data_list_without_image = load_user_data_without_image()
        formatted_user_data = ""
        for user in user_data_list_without_image:
            formatted_user_data += f"Name: {user['name']}, Gender: {user['gender']}, Religion: {user['religion']}, Job: {user['job']}\n"

        match_prompt = f"{match_finding_prompt} Here are the potential matches: {formatted_user_data}"

        try:
            match_result = call_gpt3(match_prompt)
            st.success("Date's information submitted successfully!")

            # Process GPT-3 response and display matches
            # Your logic to process and display matches

        except Exception as e:
            st.error(f"An error occurred: {e}")

    if st.button('Download User Data JSON'):
        user_data_list = load_user_data_without_image()
        st.markdown(get_table_download_link(user_data_list), unsafe_allow_html=True)

    if st.button('Download Dates Data JSON'):
        dates_data_list = load_user_data_without_image("dates_data.json")
        st.markdown(get_table_download_link(dates_data_list, "dates_data.json"), unsafe_allow_html=True)

    if 'full_prompt' not in st.session_state:
        st.session_state.full_prompt=""
    if 'gpt3_response' not in st.session_state:
        st.session_state.gpt3_response=""

    if 'user_data_list' not in st.session_state:
        st.session_state.user_data_list = load_user_data_without_image("user_data.json")
    user_data_list = st.session_state.user_data_list

    current_user = user_data_list[-1] if user_data_list else None

    if current_user:
        user_prompt = f"and prioritize matches who are {date_gender}, follow the {date_religion} religion, and work as a {date_job}."
    else:
        user_prompt = "No current user data available."
    
    button = st.button("Send Data to GPT-3.5")

    if button:
        gpt3_response = call_gpt3(user_prompt)
        st.write("OpenAI Response:", gpt3_response)
    else:
        st.error("No user data available.")

if __name__ == "__main__":
    main()
