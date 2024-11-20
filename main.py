from flask import Flask, render_template
import requests

app = Flask(__name__)

# OpenWeatherMap API key and URL
API_KEY = "007fd3ea77b65d71397dc06f76860542"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"


# Define a dictionary for weather condition emojis
weather_emojis = {
    'Clear': '☀️',
    'Clouds': '☁️',
    'Rain': '🌧️',
    'Drizzle': '🌦️',
    'Thunderstorm': '⛈️',
    'Snow': '🌨️',
    'Mist': '🌫️',
    'Haze': '🌁',
    'Fog': '🌫️'
}

# Utility function to get weather data
def get_weather_data(city="Montreal"):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  # Get temperature in Celsius
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        condition = data['weather'][0]['main']
        weather = {
            'temperature': int(data['main']['temp']),  # Absolute number
            'condition': f"{condition} {weather_emojis.get(condition, '')}",  # Add emoji dynamically
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    else:
        print(f"Error: Unable to fetch weather data (status code: {response.status_code})")
        return None


# Utility function to get forecast data
def get_forecast_data(city="Montreal"):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        forecast = [
            {
                'day': 'Tomorrow',
                'temp': int(data['list'][0]['main']['temp']),
                'condition': f"{data['list'][0]['weather'][0]['main']} {weather_emojis.get(data['list'][0]['weather'][0]['main'], '')}"
            },
            {
                'day': 'Day 2',
                'temp': int(data['list'][8]['main']['temp']),
                'condition': f"{data['list'][8]['weather'][0]['main']} {weather_emojis.get(data['list'][8]['weather'][0]['main'], '')}"
            },
            {
                'day': 'Day 3',
                'temp': int(data['list'][16]['main']['temp']),
                'condition': f"{data['list'][16]['weather'][0]['main']} {weather_emojis.get(data['list'][16]['weather'][0]['main'], '')}"
            }
        ]
        return forecast
    else:
        print(f"Error: Unable to fetch forecast data (status code: {response.status_code})")
        return None


@app.route('/')
def index():
    # Fetch weather and forecast data for the default city
    city = "Montreal"  # You can make this dynamic by passing it from the frontend
    weather_data = get_weather_data(city)
    forecast_data = get_forecast_data(city)

    if weather_data and forecast_data:
        return render_template('weather.html', weather=weather_data, forecast=forecast_data)
    else:
        return "Error fetching weather data, please try again later."


if __name__ == '__main__':
    app.run(debug=True)
