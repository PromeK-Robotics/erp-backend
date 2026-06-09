from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2, os

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])

conn = psycopg2.connect(host=os.getenv("DB_HOST"),database="postgres",user="postgres",password=os.getenv("DB_PASS"))

@app.get("/")
def root(): return {"status":"ok"}

@app.get("/commesse")
def get():
 cur=conn.cursor();cur.execute("SELECT codice,cliente,stato,avanzamento,preventivo FROM commesse")
 rows=cur.fetchall()
 return [{"codice":r[0],"cliente":r[1],"stato":r[2],"avanzamento":r[3],"preventivo":r[4]} for r in rows]

@app.post("/commesse")
def create(d:dict):
 cur=conn.cursor()
 cur.execute("INSERT INTO commesse (codice,cliente,stato,avanzamento,preventivo) VALUES (%s,%s,%s,%s,%s)",(d["codice"],d["cliente"],d.get("stato","nuova"),0,d.get("preventivo",0)))
 conn.commit()
 return {"ok":True}

@app.post("/ore")
def ore(d:dict):
 cur=conn.cursor()
 cur.execute("INSERT INTO ore (commessa,ore,costo_orario) VALUES (%s,%s,%s)",(d["commessa"],d["ore"],d["costo_orario"]))
 conn.commit()
 return {"ok":True}

@app.get("/economico/{cod}")
def eco(cod:str):
 cur=conn.cursor()
 cur.execute("SELECT SUM(ore*costo_orario) FROM ore WHERE commessa=%s",(cod,))
 costo=cur.fetchone()[0] or 0
 return {"preventivo":100000,"costo":costo,"margine":100000-costo}
