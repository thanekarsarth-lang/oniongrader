import streamlit as st
import requests
import ollama

st.set_page_config(
    page_title="WeatherGPT",
    page_icon="🌦️"
)

st.title("🌦️ WeatherGPT")
st.write("Ask AI about the weather in any city.")

# City input
city = st.text_input("📍 Enter your city")

# Question input
question = st.text_input(
    "💬 What do you want to know?",
    placeholder="Should I go for a bike ride today?"
)

if st.button("🤖 Ask WeatherGPT"):

    if city and question:

        # -----------------------------
        # 1. Find city coordinates
        # -----------------------------

        geo_url = "https://geocoding-api.open-meteo.com/v1/search"

        geo_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        geo_response = requests.get(
            geo_url,
            params=geo_params
        )

        geo_data = geo_response.json()

        if "results" not in geo_data:

            st.error("❌ City not found.")

        else:

            location = geo_data["results"][0]

            latitude = location["latitude"]
            longitude = location["longitude"]

            # -----------------------------
            # 2. Get real weather
            # -----------------------------

            weather_url = "https://api.open-meteo.com/v1/forecast"

            weather_params = {
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            }

            weather_response = requests.get(
                weather_url,
                params=weather_params
            )

            weather_data = weather_response.json()

            current = weather_data["current"]

            temperature = current["temperature_2m"]
            humidity = current["relative_humidity_2m"]
            wind = current["wind_speed_10m"]
            weather_code = current["weather_code"]

            # -----------------------------
            # 3. Show weather
            # -----------------------------

            st.subheader("🌤️ Current Weather")

            st.write(
                f"🌡️ Temperature: **{temperature} °C**"
            )

            st.write(
                f"💧 Humidity: **{humidity}%**"
            )

            st.write(
                f"💨 Wind: **{wind} km/h**"
            )

            # -----------------------------
            # 4. Send data to AI
            # -----------------------------

            prompt = f"""
You are WeatherGPT, an intelligent weather assistant.

Current weather information:

City: {city}
Temperature: {temperature} °C
Humidity: {humidity}%
Wind speed: {wind} km/h
Weather code: {weather_code}

The user asks:

{question}

Give a useful, simple and practical answer.
Use the weather information above.
Do not invent weather information that was not provided.
"""

            # -----------------------------
            # 5. Ask Gemma
            # -----------------------------

            with st.spinner("🤖 WeatherGPT is thinking..."):

                response = ollama.chat(
                    model="gemma3:4b",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

            answer = response["message"]["content"]

            # -----------------------------
            # 6. Display AI answer
            # -----------------------------

            st.subheader("🤖 WeatherGPT")

            st.write(answer)

    else:

        st.warning(
            "Please enter both a city and a question."
        )