import requests
import logging

def get_weather(location):
    try:
        api_key = "62c80855e230ea219a813a771e917f71"  
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            return (
                f"Weather in {location.title()}:\n"
                f"- Description: {description}\n"
                f"- Temperature: {temp}Celsius (feels like {feels_like}Celsius)\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s"
            )
        elif response.status_code == 404:
            return f"Location '{location}' not found."
        else:
            logging.error(f"Weather API error: {response.status_code}, Details: {response.text}")
            return "I'm having trouble fetching the weather right now. Please try again later."
    except Exception as e:
        logging.exception("Unexpected error occurred while fetching weather.")
        return "An error occurred. Please check your input or try again later."
