from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

DB = "plantas.db"

# =====================================================
# FUNCIÓN PARA OBTENER DATOS DE UNA PLANTA ESPECÍFICA
# =====================================================
def get_data(planta):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT temperatura, humedad, fecha
        FROM lecturas
        WHERE planta = ?
        ORDER BY id DESC
        LIMIT 30
    """, (planta,))
    data = c.fetchall()
    conn.close()
    return data


# =====================================================
# RUTA PRINCIPAL (DASHBOARD)
# =====================================================
@app.route("/")
def index():
    return render_template("index.html")


# =====================================================
# API PARA OBTENER DATOS DE LAS TRES PLANTAS
# =====================================================
@app.route("/api/data")
def data():
    return jsonify({
        "rene": get_data("rene"),
        "alan": get_data("alan"),
        "alessandro": get_data("alessandro")
    })


# =====================================================
# INICIAR SERVIDOR FLASK
# =====================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

