import requests
import json
import os

API_KEY = os.getenv('MY_API_KEY')

def display_city_weather(api_token):

    selected_city = "Volkhov"
    request_url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={api_token}&units=metric&lang=ru"
    
    server_response = requests.get(request_url)
    server_response.raise_for_status()       
    weather_info = server_response.json()
    
    current_temp = weather_info['main']['temp']
    perceived_temp = weather_info['main']['feels_like']
    humidity_level = weather_info['main']['humidity']
    atmospheric_pressure = weather_info['main']['pressure']
    sky_condition = weather_info['weather'][0]['description']
    wind_velocity = weather_info['wind']['speed']
        
    print(f"ТЕКУЩАЯ ПОГОДА В ВЫБРАННОМ ГОРОДЕ")
    print(f"Город: {selected_city}")
    print(f"Температура воздуха: {current_temp:.1f}°C (ощущается как {perceived_temp:.1f}°C)")
    print(f"Относительная влажность: {humidity_level}%")
    print(f"Атмосферное давление: {atmospheric_pressure} гПа")
    print(f"Скорость ветра: {wind_velocity} м/с")
    print(f"Описание погоды: {sky_condition}")


if __name__ == "__main__":
    display_city_weather(API_KEY)