import streamlit as st
import dotenv 
import langchain
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import zipfile

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

st.set_page_config(page_title = "Resume to Portfolio", page_icon = "📄")
st.title(":rainbow[AI Resume to Portfolio Generator]")

uploaded_file = st.file_uploader("Upload your Resume (pdf only)", 
                                 type = "pdf")

prompt = st.text_area("Describe the requirements to customize you portfolio", 
                      placeholder = """
                        Example
                        - Light sky-blue theme
                        - Modern and clean UI
                        - Data science related visuals
                        - Dark readable fonts
                        - Category-wise projects
                        - GitHub & LinkedIn buttons
                        - Dark / Light mode
                        """)

def text_extract(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text() + "\n"
    return text


if st.button("Generate Website"):
    if uploaded_file and prompt.strip():

        resume_text= text_extract(uploaded_file)

        final_prompt = [("""You are a powerfull web development expert. Having 10+ years of experience in web development.
                    you need to generate a proffessional Portfolio.
                    
                    STRICT RULES:
                    - You must give only html, css and java script codes.
                    - No extra explainations, comments or extra text.
                    - Must follow the below format.
                    
                    The output format should be exactly followed below format :
                    start with:
                    --html--
                    [html code]
                    --html--

                    --css--
                    [css code]
                    --css--

                    --js--
                    [java script code]
                    --js--
                         """),
                    ("user",f"""You need to use the content from {resume_text} for the portfolio
                    And follow these instructions:
                           {prompt} to generate the portfolio.""")]
        
        model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash")
        response = model.invoke(final_prompt)

        with open("file.txt","w") as file:
            file.write(response.content)

        with open("index.html","w") as file:
            file.write(response.content.split("--html--")[1])

        with open("style.css","w") as file:
            file.write(response.content.split("--css--")[1])

        with open("script.js","w") as file:
            file.write(response.content.split("--js--")[1])

        with zipfile.ZipFile("website.zip", "w") as zip:
            zip.write("index.html")
            zip.write("style.css")
            zip.write("script.js")

        st.download_button("click to download", 
                              data = open("website.zip", "rb"),
                              file_name = "Websitezip")

        st.success("successfully generated")
