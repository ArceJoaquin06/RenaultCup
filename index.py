from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar flash messages

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('Conection Uri: mysql://ud9jvwojdhecxorj:Yhm9ZPUXDoaXUX2gpLjV@b0n5dgbft6ikjmsxr1ms-mysql.services.clever-cloud.com:3306/b0n5dgbft6ikjmsxr1ms') or 'mysql://ud9jvwojdhecxorj:Yhm9ZPUXDoaXUX2gpLjV@b0n5dgbft6ikjmsxr1ms-mysql.services.clever-cloud.com:3306/b0n5dgbft6ikjmsxr1ms'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

class Equipos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_equipo = db.Column(db.String(50), nullable=False)
    deporte_equipo = db.Column(db.String(50), nullable=False)
    puntos_equipo = db.Column(db.Integer, nullable=False)
    grupo_equipo = db.Column(db.String(5), nullable=False)
    partidos_empatados = db.Column(db.Integer, nullable=False)
    partidos_ganados = db.Column(db.Integer, nullable=False)
    partidos_perdidos = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def principal():
    return render_template('Menu.html')

@app.route('/sports')
def Sports():
    return render_template('Deportes.html')

@app.route('/basket')
def Basket():
    return render_template('Basquet.html')

@app.route('/volley')
def Volley():
    return render_template('Voley.html')

@app.route('/football', methods=['GET'])
def Football():
    registros = Equipos.query.all()
    datos = []
    for registro in registros:
        datos.append({"nombre":registro.nombre_equipo, "grupo":registro.grupo_equipo, "pts":registro.puntos_equipo, "pg":registro.partidos_ganados, "pe": registro.partidos_empatados, "pp":registro.partidos_perdidos})
    return render_template('Futbol.html', datos=datos)

@app.route('/update/<id>', methods=['PUT'])
def update(id):
    update_equipo = Equipos.query.get(id)
    if not update_equipo:
        return jsonify({"error": "Equipo no encontrado"}), 404
    
    if "puntos_equipo" in request.json:
        update_equipo.puntos_equipo = request.json["puntos_equipo"]

    if "partidos_ganados" in request.json:
        update_equipo.partidos_ganados = request.json["partidos_ganados"]

    if "partidos_empatados" in request.json:
        update_equipo.partidos_empatados = request.json["partidos_empatados"]

    if "partidos_perdidos" in request.json:
        update_equipo.partidos_perdidos = request.json["partidos_perdidos"]
    
    db.session.commit()

    data_serializada = {"id": update_equipo.id, "nombre_equipo": update_equipo.nombre_equipo, "puntos_equipo": update_equipo.puntos_equipo, "partidos_ganados": update_equipo.partidos_ganados}
    return jsonify(data_serializada)

@app.route('/buscar_id', methods=['GET'])
def buscar_id():
    nombre_equipo = request.args.get('nombre')
    equipo = Equipos.query.filter_by(nombre_equipo=nombre_equipo).first()
    if equipo:
        return jsonify({"id": equipo.id})
    else:
        return jsonify({"id": None})
    
@app.route('/obtener_equipos', methods=['GET'])
def obtener_equipos():
    equipos = Equipos.query.all()
    equipos_json = [{"id": equipo.id, "nombre_equipo": equipo.nombre_equipo} for equipo in equipos]
    return jsonify(equipos_json)

@app.route('/register')
def Register():
    return render_template('Registro.html')

@app.route('/Eliminatorias')
def Eliminatorias():
    return render_template('Eliminatorias.html')

@app.route('/court')
def Court():
    return render_template('Canchas.html')

@app.route('/canteen')
def Canteen():
    return render_template('Cantina.html')

@app.route('/footballMirror')
@login_required
def Mirror():
    return render_template('FutMirror.html')

@app.route('/selectMirror')
@login_required
def Select():
    return render_template('SelectMirror.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        login_user(user)
        flash('Login successful!', 'success')
        return redirect(url_for('Select'))
    else:
        flash('Invalid username or password', 'danger')
        return redirect(url_for('Register'))

if __name__ == '__main__':
    app.run(debug=True, port=3500)