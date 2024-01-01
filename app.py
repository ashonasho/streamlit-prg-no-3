import streamlit as st
import datetime
import json
import base64

def main():
    with open("user_data.json", "r") as json_file:
        user_data_list = json.load(json_file)

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
            # Append the new user data to the existing data
            user_data_list.append(user_data)

            # Write the updated user data back to the JSON file
            with open("user_data.json", "w") as json_file:
                json.dump(user_data_list, json_file, indent=4)

            st.success("User data submitted and appended successfully!")

            # After submitting user data, create a new form to ask for date's information
            with st.form("date_info_form"):
                st.title("Date's Information")
                date_gender = st.text_input("Date's Gender", placeholder="Enter date's gender")
                date_religion = st.text_input("Date's faith community", placeholder="Enter date's religion / No religion")
                date_job = st.text_input("Date's position of employment", placeholder="Job / Student / other")
                high_preference = st.text_input("High Preference", placeholder=" Date's gender & religion / gender & job/ All")

                submit_date_info = st.form_submit_button("Submit Date's Information")

                if submit_date_info:
                    # Process and save date's information
                    st.success("Date's information submitted successfully!")

                    # Load user data from JSON file
                    with open("user_data.json", "r") as json_file:
                        user_data_list = json.load(json_file)

                    # Filter user data based on high preference
                    if "gender & religion" in high_preference:
                        filtered_data = [user for user in user_data_list if user.get("gender") == date_gender and user.get("religion") == date_religion]
                    elif "gender & job" in high_preference:
                        filtered_data = [user for user in user_data_list if user.get("gender") == date_gender and user.get("job") == date_job]
                    else:
                        filtered_data = [user for user in user_data_list if user.get("gender") == date_gender and user.get("religion") == date_religion and user.get("job") == date_job]

                    # Display filtered data to the user
                    if filtered_data:
                        st.title("Filtered Users Based on High Preference")
                        st.json(filtered_data)
                    else:
                        st.warning("No matching users found based on high preference.")

if __name__ == "__main__":
    main()
