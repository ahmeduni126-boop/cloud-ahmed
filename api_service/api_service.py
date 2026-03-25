import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://ahmed:KGVZ993ik5EQMpIMAWbmpvh9XZuyX0xI@dpg-d6t8rhq4d50c73c5c7sg-a.oregon-postgres.render.com/hello_cloud3_db_5dbw"
)

def connect_db():
    return psycopg2.connect(DATABASE_URL)

@app.route("/ziyaretciler", methods=["GET", "POST"])
def ziyaretciler():
    conn = connect_db()
    cur = conn.cursor()

    # tablo oluştur
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ziyaretciler (
            id SERIAL PRIMARY KEY,
            isim TEXT
        )
    """)

    if request.method == "POST":
        isim = request.json.get("isim")
        if isim:
            cur.execute("INSERT INTO ziyaretciler (isim) VALUES (%s)", (isim,))
            conn.commit()

    cur.execute("SELECT isim FROM ziyaretciler ORDER BY id DESC LIMIT 10")
    isimler = [row[0] for row in cur.fetchall()]

    cur.close()
    conn.close()

    return jsonify(isimler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # ✅ Render uyumlu
    app.run(host="0.0.0.0", port=port)
