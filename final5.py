# Functie om de gemiddelde statistieken te berekenen
def calculate_averages(df):
    averages = {
        "Views": round(df["Views"].mean(), 2),
        "Likes": round(df["Likes"].mean(), 2),
        "Comments": round(df["Comments"].mean(), 2),
        "Shares": round(df["Shares"].mean(), 2),
        "Engagement Rate": round(df["Engagement Rate"].mean(), 2)  # Voeg hier de gemiddelde Engagement Rate toe
    }
    return averages

# Functie om de totale sommen van de statistieken te berekenen
def calculate_totals(df):
    totals = {
        "Views": int(df["Views"].sum()),
        "Likes": int(df["Likes"].sum()),
        "Comments": int(df["Comments"].sum()),
        "Shares": int(df["Shares"].sum()),
        "Engagement Rate": "-"  # Engagement Rate is een gemiddelde, dus we laten dit leeg
    }
    return totals

# Verwerking van de video-URL's en het weergeven van statistieken
if st.button("Verwerk URL's"):
    if urls_input:
        video_urls = urls_input.splitlines()
        video_data = [get_video_data(url, url.split("/")[-1]) for url in video_urls if get_video_data(url, url.split("/")[-1])]

        if video_data:
            df = pd.DataFrame(video_data)
            df['Engagement Rate'] = pd.to_numeric(df['Engagement Rate'], errors='coerce')
            df['Engagement Rate'].fillna(0, inplace=True)
            df['Engagement Rate (%)'] = df['Engagement Rate'].apply(lambda x: f"{round(x, 2)}%")
            df = df.drop(columns=["Cover URL", "Engagement Rate"]).rename(columns={"Engagement Rate (%)": "Engagement Rate"})

            st.write("### Video Details")
            st.dataframe(df)

            # Bereken en toon de totale statistieken
            totals = calculate_totals(df)
            st.write("### Total Statistics")
            st.dataframe(pd.DataFrame([totals]))

            # Bereken en toon de gemiddelde statistieken inclusief Engagement Rate
            averages = calculate_averages(df)
            st.write("### Average Statistics")
            st.dataframe(pd.DataFrame([averages]))
        else:
            st.error("Geen geldige gegevens gevonden voor de ingevoerde video's.")
