import streamlit as st
import datetime
import json
import base64
import openai

# Set up your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"  # Replace with your actual OpenAI API key

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

# Function to call GPT-3.5 for match-finding prompts
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

    user_data_list = load_user_data()

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
        date_gender = st.radio("Your Gender", ["Male", "Female", "Other"])
        date_religion = st.selectbox("Date's Religion", options=["Hindu","Rc","Non Rc","Muslim","Buddhism"], key="date_religion" )
        date_job = st.selectbox("Date's Job",options=["Doctor","Engineer","Nurse","Software Engineer","Teacher","App developer","Farmer","Businessman","Software Developer","Coach","Qs","Architect","Banker","District coordinator","TL","HR","Dentist","Manager","Waiter","Technicians","Scientist","Care aker","Barber","AI developer","Tailor","Delivery service","House Cleaner","Driver","Attendant","Part-timer","Student","actor","Other","No job"], key=" date_job")
        high_preference = st.selectbox("High Preference", options=["gender & religion", "gender & job", "All"], key="high_preference")

        # Check if all required fields in the date form are filled
        all_date_fields_filled = all([date_gender, date_religion, date_job, high_preference])

        # Submit button for the date's form, enabled only when all fields are filled
        submit_date_info = st.form_submit_button("Submit Date's Information", disabled=not all_date_fields_filled)

    if submit_date_info:
        # Prepare a match-finding prompt
        match_finding_prompt = f"Find a match for a {date_gender} of {date_religion} religion and {date_job} job with high preference for {high_preference}"

        # Call GPT-3.5 to find a match based on the prompt
        match_result = call_gpt3_match_finding(match_finding_prompt)

        st.success("Date's information submitted successfully!")

        # Load user data again (in case new data was added)
        user_data_list = load_user_data()

        # Check preferences and find matching profiles
        matching_profiles = []
        for user in user_data_list:
            # You can use the match_result to filter profiles or suggest matches based on GPT-3.5's response
            # For example, you can use it to filter profiles by interests or other criteria.
            if high_preference == "gender & religion" and user['gender'] == date_gender and user['religion'] == date_religion:
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
