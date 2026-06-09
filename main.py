
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ INSERISCI QUI I TUOI DATI SUPABASE
conn = psycopg2.connect(
    host="db.xpjolxzococqmsaxayat.supabase.co",
    database="postgres",
    user="postgres",
    password="PromeK@#@2026"
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/commesse")
def get_commesse():
    cur = conn.cursor()
    cur.execute("SELECT codice, cliente, stato, preventivo FROM commesse")
    rows = cur.fetchall()

    return [
        {"codice": r[0], "cliente": r[1], "stato": r[2], "preventivo": r[3]}
        for r in rows
    ]

@app.post("/commesse")
def crea_commessa(data: dict):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO commesse (codice, cliente, stato, preventivo)
        VALUES (%s, %s, %s, %s)
    """, (
        data["codice"],
        data["cliente"],
        data.get("stato", "nuova"),
        data.get("preventivo", 0)
    ))

    conn.commit()
    return {"ok": True}
