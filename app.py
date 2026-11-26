from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)

api = Flask(__name__)

uri = os.getenv("MONGO_URI")

if not uri:
    raise ValueError("No se encontro MONGO_URI en el archivo .env")

conexion = MongoClient(uri)

db = conexion["CURSOS_CTPI_2026-OSCAR"]

aprendices = db["APRENDICES_CASTRO"]


@api.route("/")
def inicio():
    conexion.admin.command("ping")
    return jsonify({
        "mensaje": "Conexion exitosa a MongoDB Atlas"
    })


# Consulta 1
@api.route("/api/cantidadAprendices")
def cantidadAprendices():
    cantidad = aprendices.count_documents({})
    return jsonify({"CantidadAprendices": cantidad})


# Consulta 2
@api.route("/api/cantidadAprendices/<nivel>")
def cantidadPorNivel(nivel):
    cantidad = aprendices.count_documents({
        "NIVEL_DE_FORMACION": nivel.upper()
    })

    return jsonify({
        "Nivel de formación": nivel.upper(),
        "CantidadAprendices": cantidad
    })


# Consulta 3
@api.route("/api/programas/<nivel>")
def programas(nivel):
    resultado = aprendices.distinct("PROGRAMA", {
        "NIVEL_DE_FORMACION": nivel.upper()
    })

    return jsonify({
        "nivel de formación": nivel.upper(),
        "programas": resultado
    })


# Consulta 4
@api.route("/api/certificados/<programa>")
def certificados(programa):
    resultado = aprendices.find({
        "PROGRAMA": programa.upper(),
        "ESTADO_APRENDIZ": "Certificado"
    }, {
        "_id": 0,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    })

    return jsonify({
        "Programa": programa.upper(),
        "Aprendices_Certificados": list(resultado)
    })


# Consulta 5
@api.route("/api/porCertificar/<int:ficha>/<int:cantidad>")
def porCertificar(ficha, cantidad):

    if cantidad <= 0:
        return jsonify({
            "mensaje": "La cantidad debe ser mayor a cero"
        }), 400

    resultado = aprendices.find({
        "FICHA": ficha,
        "ESTADO_APRENDIZ": "Por certificar"
    }, {
        "_id": 0,
        "FICHA": 1,
        "PROGRAMA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    }).sort("PRIMER_APELLIDO", -1).limit(cantidad)

    return jsonify(list(resultado))


# Consulta 6
@api.route("/api/terminadaUnificacion/<programa>")
def terminadaUnificacion(programa):
    resultado = aprendices.find({
        "PROGRAMA": programa.upper(),
        "ESTADO_FICHA": "Terminada por unificación"
    }, {
        "_id": 0,
        "FICHA": 1,
        "NUMERO_DOCUMENTO": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    })

    return jsonify(list(resultado))


# Consulta 7
@api.route("/api/aprendicesPowerBI")
def aprendicesPowerBI():
    resultado = aprendices.find({
        "PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI"
    }, {
        "_id": 0,
        "PROGRAMA": 1,
        "FICHA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1
    })

    return jsonify(list(resultado))


# Consulta 8
@api.route("/api/certificadosPowerBI")
def certificadosPowerBI():
    cantidad = aprendices.count_documents({
        "PROGRAMA": "VISUALIZACION DE DATOS USANDO POWER BI",
        "ESTADO_APRENDIZ": "Certificado"
    })

    return jsonify({
        "Programa": "VISUALIZACION DE DATOS USANDO POWER BI",
        "Estado": "Certificado",
        "CantidadAprendices": cantidad
    })


# Consulta 9
@api.route("/api/aprendicesEstado/<int:ficha>/<estado>")
def aprendicesEstado(ficha, estado):

    if estado.lower() == "formación":
        estado = "Formacion"

    resultado = aprendices.find({
        "FICHA": ficha,
        "ESTADO_APRENDIZ": estado.capitalize()
    }, {
        "_id": 0,
        "FICHA": 1,
        "PROGRAMA": 1,
        "NOMBRE": 1,
        "PRIMER_APELLIDO": 1,
        "SEGUNDO_APELLIDO": 1,
        "ESTADO_APRENDIZ": 1
    })

    return jsonify(list(resultado))


if __name__ == "__main__":
    api.run(port=8000, debug=True)