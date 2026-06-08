from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv, os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

PERCORSO = os.getenv("ORDINI_PATH", "./ordini_progest/")

@app.get("/")
def root():
    return {"status":"ok"}

@app.get("/commesse")
def commesse():
    return [{"id":1,"codice":"C-001","cliente":"ABC SRL"}]

@app.post("/genera-ordine")
def genera_ordine(data: dict):
    os.makedirs(PERCORSO, exist_ok=True)

    filename = f"{PERCORSO}ORDINE_{data['commessa']}_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["TipoDoc","Cliente","Data","CodiceCommessa","Articolo","Descrizione","Quantità","Prezzo"])

        oggi = datetime.now().strftime("%Y-%m-%d")

        for r in data["righe"]:
            writer.writerow([
                "ORDINE",
                data["cliente"],
                oggi,
                data["commessa"],
                r["articolo"],
                r.get("descrizione",""),
                r["quantita"],
                r.get("prezzo",0)
            ])

    return {"file": filename}
