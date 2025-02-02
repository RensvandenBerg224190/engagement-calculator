import requests
import pandas as pd
import streamlit as st

# Haal de gebruikersnaam en wachtwoord op uit secrets
USERNAME = st.secrets["auth"]["username"]
PASSWORD = st.secrets["auth"]["password"]

# Login interface
st.title("Login")
input_username = st.text_input("Gebruikersnaam")
input_password = st.text_input("Wachtwoord", type="password")

if st.button("Inloggen"):
    if input_username == USERNAME and input_password == PASSWORD:
        st.session_state["logged_in"] = True
        st.experimental_rerun()
    else:
        st.error("Onjuiste gebruikersnaam of wachtwoord!")
        st.stop()

# Controleer of de gebruiker is ingelogd
if not st.session_state.get("logged_in", False):
    st.stop()

# Vanaf hier wordt de oorspronkelijke pagina weergegeven
st.title('TikTok Video Statistics')

# Gebruiker kan meerdere TikTok URL's invoeren
urls_input = st.text_area("Voer de TikTok video-URL's in, gescheiden door een nieuwe regel:", height=300)

if st.button("Verwerk URL's"):
    if urls_input:
        video_urls = urls_input.splitlines()
        videos = get_multiple_videos_data(video_urls)

        if videos:
            df = pd.DataFrame(videos)
            df = df.drop(columns=["Cover URL"])
            df['Engagement Rate'] = pd.to_numeric(df['Engagement Rate'], errors='coerce')
            df['Engagement Rate'].fillna(0, inplace=True)
            df['Engagement Rate (%)'] = df['Engagement Rate'].apply(lambda x: f"{round(x, 2)}%")
            df2 = df.drop(columns=["Engagement Rate"]).rename(columns={"Engagement Rate (%)": "Engagement Rate"})

            st.write("### Video Details")
            st.dataframe(df2)
        else:
            st.error("Er zijn geen geldige gegevens gevonden voor de ingevoerde video's.")
