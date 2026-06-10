from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DATI SUPABASE (METTI I TUOI)
SUPABASE_URL = "https://xpjolxzococqmsaxayat.supabase.co"
SUPABASE_KEY = "sb_secret_jZ0S33WXH-JvxtdAS_bG7w_X86TxnR5"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.get("/")
def root():
    return {"status": "ok"}

# ✅ GET COMMESSE
@app.get("/commesse")
def get_commesse():
    res = requests.get(
        f"{SUPABASE_URL}/rest/v1/commesse?select=*",
        headers=headers
    )
    return res.json()

# ✅ CREA COMMESSA
@app.post("/commesse")
def crea_commessa(data: dict):
    res = requests.post(
        f"{SUPABASE_URL}/rest/v1/commesse",
        headers=headers,
        json=data
    )
    return {"ok": True}
