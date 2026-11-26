from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

api = Flask(__name__)

conexion = MongoClient(os.getenv("MONGO_URI"))

db = conexion["CURSOS_CTPI_2026-OSCAR"]

aprendices = db["APRENDICES_CASTRO"]

@api.route("/")
def inicio():
    conexion.admin.command("ping")
    return jsonify({
        "mensaje": "Conexion exitosa a MongoDB Atlas"
    })

if __name__ == "__main__":
    api.run(port=8000, debug=True)