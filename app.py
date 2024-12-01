import streamlit as st
import json
import pandas as pd
import folium
from streamlit_folium import st_folium

# Load the JSON data
def load_json(uploaded_file):
    # Read the uploaded file as a stream and load it as JSON
    data = json.load(uploaded_file)
    return data

# Display the competitor analysis as a table
# def display_competitor_analysis(data):
#     competitors = []
#     # Check if 'competitor_analysis' exists and is in the expected format
#     competitor_analysis = data['market_insights'].get('competitor_analysis', "")
#     if competitor_analysis:
#         for competitor in competitor_analysis.split("\n"):
#             competitor_data = competitor.split(" - ")
#             if len(competitor_data) > 1:
#                 name = competitor_data[0]
#                 details = competitor_data[1]
#                 competitors.append([name, details])
    
#     if competitors:
#         df_competitors = pd.DataFrame(competitors, columns=["Competitor", "Details"])
#         st.subheader("Competitor Analysis")
#         st.table(df_competitors)
#     else:
#         st.warning("No competitor data found or format is incorrect.")

# Display recommendations with map
def display_recommendations(data):
    recommendations = data['market_insights'].get('recommendations', [])
    if recommendations:
        map_center = [recommendations[0]['latitude'], recommendations[0]['longitude']]
        m = folium.Map(location=map_center, zoom_start=14)

        st.subheader("Existing Establishment")
        for rec in recommendations:
            folium.Marker(
                location=[rec['latitude'], rec['longitude']],
                popup=f"{rec.get('name', 'Unknown Name')} - Rating: {rec.get('rating', 'N/A')} - Sentiment Score: {rec.get('sentiment_score', 'N/A')}",
            ).add_to(m)

        st_folium(m, width=700, height=500)
    else:
        st.warning("No restaurant recommendations found.")

# Display opportunities as a section
def display_opportunities(data):
    opportunities = data['market_insights'].get('opportunities', "")
    if opportunities:
        st.subheader("Business Opportunities")
        st.markdown(opportunities)
    else:
        st.warning("No business opportunities found.")

# Streamlit app
def main():
    st.title("Market Insights for Food & Beverage in Belgaum")
    
    # Upload JSON file
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    
    if uploaded_file is not None:
        # Pass the uploaded file directly to the load_json function
        data = load_json(uploaded_file)
        
        # Display market insights
        location = data['market_insights'].get('location', 'Unknown Location')
        st.subheader("Location: " + location)
        
        # Display competitor analysis as a table
        # display_competitor_analysis(data)
        
        # Display restaurant recommendations with map
        display_recommendations(data)
        
        # Display business opportunities
        display_opportunities(data)
    
if __name__ == "__main__":
    main()
