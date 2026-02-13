from flask import Flask
import requests
import datetime

app = Flask(__name__)

# Координаты Зеленограда (можно найти через любой геокодер)
ZELENGRAD_LAT = 55.9825
ZELENGRAD_LON = 37.1814

def get_zelgrad_temperature():
    """
    Получение реальной температуры через Open-Meteo API (без API ключа)
    Open-Meteo — бесплатный API для некоммерческого использования
    """
    try:
        # Open-Meteo API endpoint для текущей погоды
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": ZELENGRAD_LAT,
            "longitude": ZELENGRAD_LON,
            "current_weather": True,
            "timezone": "Europe/Moscow",
            "wind_speed_unit": "ms"  # метры в секунду
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            weather = data['current_weather']
            
            temperature = weather['temperature']
            windspeed = weather['windspeed']
            weather_code = weather.get('weathercode', 0)
            
            # Коды погоды WMO (упрощенно)
            weather_desc = {
                0: "Ясно",
                1: "Преимущественно ясно",
                2: "Переменная облачность",
                3: "Пасмурно",
                45: "Туман",
                48: "Изморозь",
                51: "Легкая морось",
                61: "Небольшой дождь",
                63: "Дождь",
                71: "Небольшой снег",
                73: "Снег",
                95: "Гроза"
            }.get(weather_code, "Разная облачность")
            
            return {
                'temp': round(temperature, 1),
                'windspeed': windspeed,
                'description': weather_desc,
                'source': 'Open-Meteo'
            }
        else:
            return {'error': f'API error: {response.status_code}'}
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def home():
    weather = get_zelgrad_temperature()
    
    if 'error' in weather:
        return f"""
        <html>
            <head><title>Погода в Зеленограде</title></head>
            <body style="font-family: Arial; text-align: center; margin-top: 50px;">
                <h1>🌡️ Ошибка получения данных</h1>
                <p>{weather['error']}</p>
                <p><small>Попробуйте обновить страницу позже</small></p>
            </body>
        </html>
        """
    
    return f"""
    <html>
        <head><title>Погода в Зеленограде</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h1>🌡️ Текущая погода в Зеленограде</h1>
            <div style="font-size: 72px; margin: 30px;">
                {weather['temp']}°C
            </div>
            <div style="font-size: 24px; margin: 20px; color: #666;">
                {weather['description']}
            </div>
            <div style="font-size: 16px; margin: 10px;">
                Ветер: {weather['windspeed']} м/с
            </div>
            <p><small>Данные: {weather['source']} (бесплатно, без API ключа)</small></p>
            <p><small>Обновлено: {datetime.datetime.now().strftime('%H:%M:%S')}</small></p>
            <p><a href="/debug">Debug: сырые данные</a></p>
        </body>
    </html>
    """

@app.route('/debug')
def debug():
    """Отладочная страница с сырыми данными от API"""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": ZELENGRAD_LAT,
            "longitude": ZELENGRAD_LON,
            "current_weather": True,
            "timezone": "Europe/Moscow"
        }
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)