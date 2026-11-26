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


# Consulta 1.
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


if __name__ == "__main__":
    api.run(port=8000, debug=True)