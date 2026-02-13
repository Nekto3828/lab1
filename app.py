from flask import Flask
import datetime
import mweather

app = Flask(__name__)

def get_zelgrad_temperature():
    """
    Получение температуры через библиотеку mweather (без API ключа)
    """
    try:
        # Библиотека mweather не требует ключей
        # Возвращает словарь с данными
        weather_data = mweather.weather(
            city="Зеленоград", 
            output="json", 
            lang="ru"
        )
        
        # Проверяем, что данные корректны
        if weather_data and 'temp' in weather_data:
            # Извлекаем числовое значение температуры из строки типа "10°C"
            temp_str = weather_data['temp']
            # Оставляем только цифры и точку
            import re
            temp_value = re.findall(r"[-+]?\d*\.?\d+", temp_str)[0]
            
            return {
                'temp': float(temp_value),
                'weather': weather_data.get('weather', 'Неизвестно'),
                'response_time': weather_data.get('response-time', 0),
                'source': 'mweather'
            }
        else:
            return {'error': 'Не удалось получить данные от mweather'}
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
                {weather['weather']}
            </div>
            <p><small>Данные: {weather['source']} (библиотека-обертка)</small></p>
            <p><small>Время ответа: {weather['response_time']} сек</small></p>
            <p><small>Обновлено: {datetime.datetime.now().strftime('%H:%M:%S')}</small></p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
