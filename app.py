from flask import Flask
import requests
import datetime
import config

app = Flask(__name__)

def get_zelgrad_temperature():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?id={config.CITY_ID}&appid={config.API_KEY}&units=metric"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            description = data['weather'][0]['description']
            return {
                'temp': round(temperature, 1),
                'feels_like': round(feels_like, 1),
                'description': description.capitalize()
            }
        else:
            return {'error': f'API error: {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def home():
    weather = get_zelgrad_temperature()
    
    if 'error' in weather:
        return f"<h1>Ошибка получения данных: {weather['error']}</h1>"
    
    return f"""
    <html>
        <head><title>Погода в Зеленограде</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🌡️ Текущая погода в Зеленограде</h1>
            <div style="font-size: 72px; margin: 30px;">
                {weather['temp']}°C
            </div>
            <div style="font-size: 24px; margin: 20px; color: #666;">
                Ощущается как: {weather['feels_like']}°C
            </div>
            <div style="font-size: 20px; margin: 20px;">
                {weather['description']}
            </div>
            <p><small>Данные OpenWeatherMap</small></p>
            <p><small>Обновлено: {datetime.datetime.now().strftime('%H:%M:%S')}</small></p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)