from typing import List

from fastapi import FastAPI, Path, Request

from schemas import MerchantCreate, MerchantOut, MerchantUpdate
from stores import MemoryStore, SQLiteStore


app = FastAPI(title="Merchant CRUD Service")
memory_store = MemoryStore()
db_store = SQLiteStore("merchants.db")


@app.get("/")
def root(request: Request):
    base = str(request.base_url).rstrip("/")
    return {
        "service": "Merchant CRUD Service",
        "non_persistent": f"{base}/memory/merchants",
        "persistent": f"{base}/db/merchants",
        "docs": f"{base}/docs",
    }


@app.get("/memory/merchants", response_model=List[MerchantOut])
def list_memory_merchants():
    return memory_store.list()


@app.post("/memory/merchants", response_model=MerchantOut, status_code=201)
def create_memory_merchant(payload: MerchantCreate):
    return memory_store.create(payload)


@app.get("/memory/merchants/{merchant_id}", response_model=MerchantOut)
def get_memory_merchant(merchant_id: int = Path(..., ge=1)):
    return memory_store.get(merchant_id)


@app.put("/memory/merchants/{merchant_id}", response_model=MerchantOut)
def update_memory_merchant(merchant_id: int, payload: MerchantUpdate):
    return memory_store.update(merchant_id, payload)


@app.delete("/memory/merchants/{merchant_id}", status_code=204)
def delete_memory_merchant(merchant_id: int):
    memory_store.delete(merchant_id)
    return None


@app.get("/db/merchants", response_model=List[MerchantOut])
def list_db_merchants():
    return db_store.list()


@app.post("/db/merchants", response_model=MerchantOut, status_code=201)
def create_db_merchant(payload: MerchantCreate):
    return db_store.create(payload)


@app.get("/db/merchants/{merchant_id}", response_model=MerchantOut)
def get_db_merchant(merchant_id: int = Path(..., ge=1)):
    return db_store.get(merchant_id)


@app.put("/db/merchants/{merchant_id}", response_model=MerchantOut)
def update_db_merchant(merchant_id: int, payload: MerchantUpdate):
    return db_store.update(merchant_id, payload)


@app.delete("/db/merchants/{merchant_id}", status_code=204)
def delete_db_merchant(merchant_id: int):
    db_store.delete(merchant_id)
    return None


