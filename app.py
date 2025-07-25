
import streamlit as st
from agent.agent import Agent
from utils.template_engine import load_templates, fill_template

from dotenv import load_dotenv

load_dotenv()

def main():
    st.title("Fusion Focus (Agents System)")

    option = st.selectbox("Choose an option", ["Write Personalized Email"])

    if option == "Write Personalized Email":
        lead_source = st.radio("What type of lead source?", ("LinkedIn", "YouTube Channel"))

        if lead_source == "LinkedIn":
            linkedin_url = st.text_input("Paste the LinkedIn profile URL")
            service_to_sell = st.text_input("What are you selling?")
            
            if st.button("Generate Email"):
                if linkedin_url and service_to_sell:
                    with st.spinner("Scraping LinkedIn profile and generating email..."):
                        goal = f"Extract the LinkedIn profile information for {linkedin_url} to generate a personalized email for selling {service_to_sell}."
                        agent = Agent(goal, service_to_sell=service_to_sell)
                        email = agent.run(linkedin_url)
                    
                    if email:
                        st.success("Email generated successfully!")
                        st.subheader("Generated Email")
                        st.write(email)
                        
                        save_email(linkedin_url.split('/')[-1], email) # Using part of URL as lead name
                    else:
                        st.error("Failed to generate email.")
                else:
                    st.warning("Please provide both LinkedIn URL and the service you are selling.")

        elif lead_source == "YouTube Channel":
            youtube_url = st.text_input("Paste the YouTube channel link")
            service_to_sell = st.text_input("What are you selling?")
            use_template = st.radio("Do you want to use a predefined template?", ("No", "Yes"))

            template_content = None
            if use_template == "Yes":
                templates = load_templates()
                template_choice = st.selectbox("Choose a template", list(templates.keys()))
                template_content = templates[template_choice]


            if st.button("Generate Email"):
                if youtube_url and service_to_sell:
                    with st.spinner("Scraping YouTube channel and generating email..."):
                        goal = "Extract the YouTube channel owner's name, description, latest video title and description."
                        agent = Agent(goal, service_to_sell=service_to_sell, template_content=template_content)
                        email = agent.run(youtube_url)
                    
                    if email:
                        st.success("Email generated successfully!")
                        st.subheader("Generated Email")
                        st.write(email)
                        
                        save_email(youtube_url.split('/')[-1], email) # Using part of URL as lead name
                    else:
                        st.error("Failed to generate email.")
                else:
                    st.warning("Please provide both YouTube URL and the service you are selling.")

def save_email(lead_name, email_content):
    import os
    from datetime import datetime
    directory = f"emails/{lead_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{lead_name}_{timestamp}.txt"
    file_path = os.path.join(directory, filename)
    
    with open(file_path, "w") as f:
        f.write(email_content)
    st.success(f"Email saved to {file_path}")

if __name__ == "__main__":
    main()
