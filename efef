import streamlit as st
import datetime
import json
import base64

st.title("Let's Date")
st.header("In the world of our Dating App, possibilities are endless. Discover the chemistry, embrace the excitement, and let your perfect date unfold in style.")

name = st.text_input("Your name", placeholder="Short name / Your name")
st.write("Welcome", name)

# Dictionary to store user data
user_data = {"name": name}

def main():
    # Check if the user has uploaded an image
    if "image" not in user_data:
        st.title("Please upload your image.")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            # Encode image to base64
            image_data = base64.b64encode(uploaded_file.read()).decode("utf-8")

            # Display image
            st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
            st.write("")
            st.write("Classifying... (add your image processing logic here)")

            # Include image data in user data dictionary
            user_data["image"] = image_data

    # Ask for additional inputs
    firstname = st.text_input("Firstname", placeholder="Enter your first name")
    secondname = st.text_input("Secondname", placeholder="Enter your second name / No second name")
    birthdate = st.date_input("Birth Date", format="DD.MM.YYYY")
    religion = st.text_input("Faith community", placeholder="Enter your religion / No religion")
    job = st.text_input("Position of employment", placeholder="Job / Student / other")
    gender = st.radio("Your Gender", ["Male", "Female"])
    height = st.number_input("Your Height", value=None, placeholder="Enter Your Height in feet ")
    yourinterests = st.text_input("Your Interests", placeholder="Music type, Dance, Sports, and etc")

    # Update user data dictionary with additional inputs
    user_data.update({
        "firstname": firstname,
        "secondname": secondname,
        "birthdate": str(birthdate),
        "religion": religion,
        "job": job,
        "gender": gender,
        "height": height,
        "interests": yourinterests
    })

    # Submit button and validation
    if st.button("Submit") and all(value and value.strip() for value in user_data.values()):
        # Serialize dictionary to JSON string
        user_json = json.dumps(user_data, indent=4)

        # Write JSON string to a file
        with open("user_data.json", "w") as json_file:
            json_file.write(user_json)

        st.success("User data submitted successfully!")
    elif "image" in user_data:
        st.warning("Please fill in all the required fields.")

if __name__ == "__main__":
    main()
