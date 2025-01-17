from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'Chennai' 

    API_KEY = "your_api_here"
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    
    
    source = requests.get(url)
    values = source.json()

    data = {
        "country_code": str(values['sys']['country']),
        "coordinate": f"{values['coord']['lon']} {values['coord']['lat']}",
        "temp_cel": celsius(values['main']['temp']) + ' °C',
        "pressure": str(values['main']['pressure']),
        "temp_max": celsius(values['main']['temp_max']) + '°C',
        "humidity": str(values['main']['humidity']),
        "cityname": str(city),
    }
    
    return render_template('index.html', data=data)

def celsius(temp):
    return str(round(float(temp) - 273.15,2))  

if __name__ == '__main__':
    app.run()
