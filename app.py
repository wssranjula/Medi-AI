from langchain_openai import ChatOpenAI , AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import streamlit as st
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


def get_response(transcript):


    template = """You are expert information extractor. your goal is to extract information from below  {transcirpt} /n
                and give it in the following format
                '''  
    "PatientName": "",  
    "PatientAge": "",
    "DoctorName": "",  
    "ClinicName": "",  
    "Date": ",  
    "Time": "",  
    "Duration": "",  
    "Symptoms": {  
        "Fatigue": "",  
        "Headaches": "",  
        "Dizziness": "",  
        "VisionChanges": "",  
        "WeightLoss": "",  
        "AppetiteChanges": "",  
        "SleepPatterns": "",  
        "MusclePain": "",  
        "JointPain": ""  
    },  
    "MedicalHistory": {  
        "ChronicConditions": "",  
        "MedicationControl": ""  
    },  
    "CurrentMedications": {  
        "Diabetes": "",  
        "Supplements": ""  
    },  
    "Allergies": "",  
    "RecentTravel": "",  
    "ContactWithSickIndividuals": "",  
    "StressLevels": " ",  
    "PlannedTests": [  
        "Potential infections",  
        "Blood count",  
        "Thyroid function",  
        "Mental health evaluation"  
    ],  
    "PatientInstructions": {  
        "Rest": "",  
        "Diet": ""  
    }  
    }  


                """

    prompt = ChatPromptTemplate.from_template("""You are expert information extractor. your goal is to extract information below  {transcirpt}
                                            extract information in this {format}
                                            If the information is not available, please leave the field empty.Provide the final output in JSON format.
                                            """)
    model = ChatOpenAI(api_key= OPENAI_API_KEY ,model="gpt-3.5-turbo")
    # model  = ChatGoogleGenerativeAI(
    #         model="gemini-2.5-pro-exp-03-25",
    #         temperature=0,
    #         max_tokens=None,
    #         timeout=30,  # Set explicit timeout
    #         max_retries=3,
    #         api_key=GOOGLE_API_KEY
    #     )

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    res = chain.invoke({"transcirpt": transcript , "format": template})
    return res
# print(res)
def load_data(data):

    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    texts = text_splitter.create_documents(data)
    return texts



transcript = """

Call Transcript Between Dr. Smith and Client Jane Doe
Date: [Insert Date]
Time: [Insert Time]
Duration: Approximately 25 minutes

Dr. Smith: Good afternoon, thank you for calling [Insert Clinic Name]. This is Dr. Smith speaking. May I have your full name, please?

Jane Doe: Hi, Dr. Smith. My name is Jane Doe.

Dr. Smith: Hello, Jane. It's nice to meet you over the phone. Before we proceed, could you please confirm your date of birth for our records?

Jane Doe: Sure, it's [Insert Date of Birth].

Dr. Smith: Thank you, Jane. How are you feeling today?

Jane Doe: Hi, Dr. Smith. Honestly, I've been better. I've been experiencing some symptoms that are quite concerning.

Dr. Smith: I'm sorry to hear that. Just to ensure I have all your information updated, may I ask what your occupation is and if you have any known medical conditions?

Jane Doe: I work as an accountant, and I have type 2 diabetes, but it's generally well-managed.

Dr. Smith: Thank you for that information. Now, let's go through your symptoms so I can get a better understanding of what might be going on. Can you describe what you've been experiencing?

Jane Doe: Sure, for the past two weeks, I've been feeling very fatigued, even after a good night's sleep. I have also been experiencing persistent headaches and occasional dizziness.

Dr. Smith: I see. Have there been any changes in your vision or any sensitivity to light?

Jane Doe: Now that you mention it, yes. Sometimes the light does seem too harsh, and my vision gets a bit blurry.

Dr. Smith: Alright, any fever or weight changes during this period?

Jane Doe: No fever, but I've lost a few pounds without really trying.

Dr. Smith: Understood. Have you noticed any changes in your appetite or eating habits?

Jane Doe: My appetite has decreased somewhat, and there are times when I feel nauseous.

Dr. Smith: What about your sleep patterns? Any difficulty falling or staying asleep?

Jane Doe: I've had some trouble falling asleep, and I often wake up in the middle of the night.

Dr. Smith: Okay, we'll make a note of that. Have you experienced any muscle or joint pain?

Jane Doe: My muscles do feel sore, and my joints, especially in my hands and knees, have been achy.

Dr. Smith: Have you had any recent injuries or infections?

Jane Doe: No, nothing like that.

Dr. Smith: How about your stress levels? Any significant changes in your personal or professional life?

Jane Doe: It's been quite stressful at work lately, more than usual.

Dr. Smith: Stress can certainly impact your health. Are you currently taking any medications or supplements?

Jane Doe: Yes, I take metformin for my diabetes and a daily multivitamin.

Dr. Smith: Any allergies to medications or foods?

Jane Doe: No known allergies.

Dr. Smith: Have you traveled anywhere recently or been in contact with anyone who was sick?

Jane Doe: No recent travel, and I haven't knowingly been around anyone who's ill.

Dr. Smith: Based on what you've told me, we need to run some tests to rule out possible causes. We'll look into potential infections, check your blood count, and assess your thyroid function, among other things. It might also be helpful to evaluate your mental health, as stress can manifest in physical symptoms. How does that sound?

Jane Doe: That sounds thorough, Dr. Smith. I just want to understand what's going on and feel better.

Dr. Smith: Absolutely, we'll do everything we can to get to the bottom of this. After we get the test results, we'll create a care plan tailored to your needs. In the meantime, try to get some rest and focus on a balanced diet to support your overall health.

Jane Doe: I will, thank you for your help, Dr. Smith.

Dr. Smith: It's my pleasure. We'll be in touch soon with your test results and next steps. Take care, Jane.

Jane Doe: You too, goodbye.

Dr. Smith: Goodbye.

[End of Call]
"""

