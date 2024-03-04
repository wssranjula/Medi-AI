import streamlit as st
import json

# Assuming the get_response function is defined in a module named 'response_generator'
from app import get_response

# Streamlit page configuration
st.set_page_config(page_title="Medical Transcript Analysis", layout="wide")

# Title for the Streamlit app
st.title("Medical Transcript Analysis")

# File uploader allows user to add their own .txt file
uploaded_file = st.file_uploader("Choose a .txt file", type="txt")

if uploaded_file is not None:
    # To read file as string:
    transcript = str(uploaded_file.read(), "utf-8")
    # Display the contents of the file
    st.text_area("Transcript", transcript, height=250)

    # Button to get response
    if st.button("Get Data"):
        with st.spinner('Processing...'):
        # Call the get_response function from the response_generator module
            response = get_response(transcript)
            if '```' in response:
                cleaned_response = "\n".join(response.split("```")[1].split("```")[0].split("\n")[1:-1])
            
            else:
                # Handle the case where the delimiter is not found, perhaps by setting cleaned_response to the entire response or some default value
                cleaned_response = response  
            
            # Assuming the response is a JSON string, load it into a dictionary
            response_data = json.loads(cleaned_response)
            print(response_data)
            
            # Display the form with the information from the response
            st.subheader("Extracted Information")
            with st.form(key='information_form'):
                st.text_input("Patient Name", value=response_data.get("PatientName", ""))
                st.text_input("Doctor Name", value=response_data.get("DoctorName", ""))
                st.text_input("Clinic Name", value=response_data.get("ClinicName", ""))
                st.text_input("Date", value=response_data.get("Date", ""))
                st.text_input("Time", value=response_data.get("Time", ""))
                st.text_input("Duration", value=response_data.get("Duration", ""))
                
                # For nested dictionaries like Symptoms, iterate over the keys and values
                st.subheader("Symptoms")
                for symptom, description in response_data.get("Symptoms", {}).items():
                    st.text_input(symptom, value=description)
                
                # Similar approach for MedicalHistory, CurrentMedications, and PatientInstructions
                st.subheader("Medical History")
                for key, value in response_data.get("MedicalHistory", {}).items():
                    st.text_input(key, value=value)
                
                st.subheader("Current Medications")
                for medication, details in response_data.get("CurrentMedications", {}).items():
                    st.text_input(medication, value=details)
                
                st.subheader("Patient Instructions")
                for instruction, details in response_data.get("PatientInstructions", {}).items():
                    st.text_input(instruction, value=details)
                
                # For lists like PlannedTests, display each item on a new line
                st.subheader("Planned Tests")
                planned_tests = response_data.get("PlannedTests", [])
                for test in planned_tests:
                    st.text_input(test, value=test)
                
                # Display non-iterable fields
                st.text_area("Allergies", value=response_data.get("Allergies", ""))
                st.text_area("Recent Travel", value=response_data.get("RecentTravel", ""))
                st.text_area("Contact With Sick Individuals", value=response_data.get("ContactWithSickIndividuals", ""))
                st.text_area("Stress Levels", value=response_data.get("StressLevels", ""))
                
                # Form submission button (does nothing here as we're just displaying data)
                st.form_submit_button("Update Information")
                                # Button to reset the page
                if st.button("Reset Page"):
                    st.experimental_rerun()