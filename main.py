from flask import Flask, render_template

app = Flask(__name__)

# Sample weather data - in a real app, this would come from an API
weather_data = {
    'temperature': 22,
    'condition': 'Sunny',
    'humidity': 45,
    'wind_speed': 15
}

weather_icons = {
    'Sunny': '☀️',
    'Cloudy': '☁️',
    'Rainy': '🌧️',
    'Stormy': '⛈️',
    'Snowy': '🌨️'
}
forecast_data = [
    {'day': 'Tomorrow', 'temp': 24, 'condition': 'Sunny'},
    {'day': 'Day 2', 'temp': 20, 'condition': 'Cloudy'},
    {'day': 'Day 3', 'temp': 18, 'condition': 'Rainy'}
]

@app.route('/')
def index():
    return render_template('weather.html',
                         weather=weather_data,
                         forecast=forecast_data)

if __name__ == '__main__':
    app.run(debug=True)