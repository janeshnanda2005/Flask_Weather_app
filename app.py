from flask import Flask, render_template,request,url_for,redirect
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    code = db.Column(db.String(5))
    coor = db.Column(db.String(100),nullable=False)
    tempcel = db.Column(db.String(100),nullable = False)
    cityname = db.Column(db.String(50))

with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city = request.form['city']
    else:
        city = 'chennai' 

    API_KEY = "48a90ac42caa09f90dcaeee4096b9e53"
    
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    
    
    source = requests.get(url)
    values = source.json()

    code = str(values['sys']['country'])
    coor = f"{values['coord']['lon']} {values['coord']['lat']}"
    tempcel = celsius(values['main']['temp'])
    cityname = str(city)

    new_user = User(code=code,coor=coor,tempcel=tempcel,cityname=cityname)
    db.session.add(new_user)
    db.session.commit()


    data = {
        "country_code":code,
        "coordinate": coor,
        "temp_cel": tempcel+ ' °C',
        "pressure": str(values['main']['pressure']),
        "temp_max": celsius(values['main']['temp_max']) + '°C',
        "humidity": str(values['main']['humidity']),
        "cityname": cityname,
    }
    
    
    return render_template('index.html', data=data)

@app.route('/DB')
def listdb():
    post = User.query.all() 
    return render_template('db.html',post=post)

@app.route('/delete/<int:user_id>',methods=['POST'])
def delete(user_id):
    userto = User.query.get(user_id)
    if userto:
        db.session.delete(userto)
        db.session.commit()
    return redirect(url_for('weather'))


def celsius(temp):
    return str(round(float(temp) - 273.15,2))  

if __name__ == '__main__':
    app.run()
