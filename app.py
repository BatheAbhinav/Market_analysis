import streamlit as st
import json
import pandas as pd
import folium
from folium import Icon
from streamlit_folium import st_folium

# Load the JSON data
def load_json(uploaded_file):
    # Read the uploaded file as a stream and load it as JSON
    data = json.load(uploaded_file)
    return data

# Display recommendations with map
def display_recommendations(data):
    recommendations = data['market_insights'].get('recommendations', [])
    if recommendations:
        map_center = [recommendations[0]['latitude'], recommendations[0]['longitude']]
        m = folium.Map(location=map_center, zoom_start=14)

        st.subheader("Existing Establishment")
        for rec in recommendations:
            # You can use the default icon or customize it
            folium.Marker(
                location=[rec['latitude'], rec['longitude']],
                popup=f"{rec.get('name', 'Unknown Name')} - Rating: {rec.get('rating', 'N/A')} - Sentiment Score: {rec.get('sentiment_score', 'N/A')}",
                icon=Icon(color='blue', icon='info-sign')  # Example of a custom marker
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
    st.title("Market Insights By Gemini 1.5 Flash")
    
    # Upload JSON file
    uploaded_file = st.file_uploader("Upload JSON File", type=["json"])
    
    if uploaded_file is not None:
        # Pass the uploaded file directly to the load_json function
        data = load_json(uploaded_file)
        
        # Display market insights
        location = data['market_insights'].get('location', 'Unknown Location')
        st.subheader("Location: " + location)
        
        # Display restaurant recommendations with map
        display_recommendations(data)
        
        # Display business opportunities
        display_opportunities(data)

if __name__ == "__main__":
    main()
