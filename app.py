from flask import Flask, render_template, request, session, redirect, url_for
from random import shuffle

app = Flask(__name__)
app.secret_key = "clave_trivia"

preguntas = [
    ("¿Qué país ganó el Mundial 2006?", ["Italia", "Francia", "Brasil", "Alemania"], "Italia"),
    ("¿Quién fue el capitán de Argentina en el Mundial 2014?", ["Lionel Messi", "Ángel Di María", "Emiliano Martínez", "Julián Álvarez"], "Lionel Messi"),
    ("¿En qué país se jugó el Mundial 2010?", ["Qatar", "Rusia", "Brasil", "Sudáfrica"], "Sudáfrica"),
    ("¿Cada cuántos años se juega un Mundial?", ["Cada 2 años", "Cada 3 años", "Cada 4 años", "Cada 5 años"], "Cada 4 años"),
    ("¿Qué selección ganó el Mundial 2018?", ["Francia", "Croacia", "Argentina", "España"], "Francia"),
    ("¿Qué países serán sede del Mundial 2026?", ["Argentina, Brasil y Uruguay", "Estados Unidos, México y Canadá", "España, Portugal y Marruecos", "Italia, Francia y Alemania"], "Estados Unidos, México y Canadá"),
    ("¿Cuántas selecciones participarán en el Mundial 2026?", ["32", "40", "48", "64"], "48"),
    ("¿Qué jugador español hizo un gol en la final del Mundial 2010?", ["Andrés Iniesta", "Xavi Hernandez", "Carles Puyol", "Sergio Ramos"], "Andrés Iniesta"),
    ("¿Qué selección perdió la final del Mundial 1986 contra Argentina?", ["Alemania", "Brasil", "Croacia", "Países Bajos"], "Alemania"),
    ("¿Quién hizo el famoso gol de Palomita en Brasil 2014?", ["David Villa", "Cristiano Ronaldo", "Wayne Rooney", "Van Persie"], "Van Persie"),
    ("¿Qué país ganó el primer Mundial de fútbol en 1930?", ["Uruguay", "Argentina", "Italia", "Brasil"], "Uruguay")
]

def controlar_respuesta(respuesta, correcta):
    return respuesta == correcta

@app.route("/")
def inicio():
    session["numero_pregunta"] = 0
    session["puntaje"] = 0
    return render_template("index.html")

@app.route("/pregunta", methods=["GET", "POST"])
def pregunta():
    if request.method == "POST":
        respuesta = request.form["respuesta"]
        correcta = session["correcta"]

        if controlar_respuesta(respuesta, correcta):
            session["puntaje"] += 1

        session["numero_pregunta"] += 1

    numero = session["numero_pregunta"]

    if numero >= len(preguntas):
        return redirect(url_for("resultado"))

    texto, opciones, correcta = preguntas[numero]
    opciones_copia = opciones[:]
    shuffle(opciones_copia)

    session["correcta"] = correcta

    return render_template("pregunta.html", pregunta=texto, opciones=opciones_copia, numero=numero + 1, total=len(preguntas))

@app.route("/resultado")
def resultado():
    puntaje = session["puntaje"]
    total = len(preguntas)
    porcentaje = (puntaje / total) * 100

    if porcentaje == 100:
        mensaje = "¡Excelente! No tuviste ningún error."
    elif porcentaje >= 60:
        mensaje = "¡Buen trabajo! Aprobaste la trivia."
    else:
        mensaje = "Podés hacerlo mejor, ¡seguí intentando!"

    return render_template("resultado.html", puntaje=puntaje, total=total, porcentaje=porcentaje, mensaje=mensaje)

if __name__ == "__main__":
    app.run(debug=True)