# Test Merchant CRUD 

## Struktur
- `main.py`: definisi app FastAPI + routing.
- `schemas.py`: model Pydantic (`MerchantCreate`, `MerchantUpdate`, `MerchantOut`).
- `stores.py`: store memory & SQLite (CRUD).
- `requirements.txt`: dependensi.
- `merchants.db`: file SQLite (dibuat otomatis jika belum ada).

## Endpoint utama
- Root info: `GET /` (link lengkap ke memory, db, docs)
- Docs interaktif: `GET /docs`
- Memory (non-persistent):
  - `GET /memory/merchants`
  - `POST /memory/merchants`
  - `GET /memory/merchants/{id}`
  - `PUT /memory/merchants/{id}`
  - `DELETE /memory/merchants/{id}`
- SQLite (persistent):
  - `GET /db/merchants`
  - `POST /db/merchants`
  - `GET /db/merchants/{id}`
  - `PUT /db/merchants/{id}`
  - `DELETE /db/merchants/{id}`

## Cara Run (Mac/Linux)
## Jika sudah ada venv nya maka tinggal langsung saja aktifkan
```bash
python3 -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Cara Run (Windows)
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1 
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Lalu buka:
- Root info: http://127.0.0.1:8000/
- Docs: http://127.0.0.1:8000/docs

## Contoh curl (SQLite / persistent)
```bash
# Create
curl -X POST http://127.0.0.1:8000/db/merchants \
  -H "Content-Type: application/json" \
  -d '{"name":"Toko A","description":"pakai DB"}'

# List
curl http://127.0.0.1:8000/db/merchants

# Update id=1
curl -X PUT http://127.0.0.1:8000/db/merchants/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Toko A Update","description":"ubah"}'

# Delete id=1
curl -X DELETE http://127.0.0.1:8000/db/merchants/1
```

## Contoh curl (Memory / non-persistent)
```bash
curl -X POST http://127.0.0.1:8000/memory/merchants \
  -H "Content-Type: application/json" \
  -d '{"name":"Toko X","description":"contoh memory"}'

curl http://127.0.0.1:8000/memory/merchants
```

## Details
- Mode memory (non-persistent) akan kosong lagi setelah server dimatikan.
- Mode SQLite (persistent) akan menyimpan data selama file `merchants.db` tidak dihapus.
- Jika port 8000 dipakai, ganti dengan `--port yang ready seperti 8001/8002` dan akses URL sesuai port baru.


