import sqlite3
import threading
from typing import Dict, List

from fastapi import HTTPException

from schemas import MerchantCreate, MerchantOut, MerchantUpdate


class MemoryStore:
    def __init__(self) -> None:
        self._data: Dict[int, MerchantOut] = {}
        self._lock = threading.Lock()
        self._next_id = 1

    def list(self) -> List[MerchantOut]:
        return list(self._data.values())


    def get(self, merchant_id: int) -> MerchantOut:
        try:
            return self._data[merchant_id]
        except KeyError:
            raise HTTPException(status_code=404, detail="Merchant not found")

    def create(self, payload: MerchantCreate) -> MerchantOut:
        with self._lock:
            merchant = MerchantOut(id=self._next_id, **payload.dict())
            self._data[self._next_id] = merchant
            self._next_id += 1
        return merchant

    def update(self, merchant_id: int, payload: MerchantUpdate) -> MerchantOut:
        with self._lock:
            if merchant_id not in self._data:
                raise HTTPException(status_code=404, detail="Merchant not found")
            updated = MerchantOut(id=merchant_id, **payload.dict())
            self._data[merchant_id] = updated
        return updated

    def delete(self, merchant_id: int) -> None:
        with self._lock:
            if merchant_id not in self._data:
                raise HTTPException(status_code=404, detail="Merchant not found")
            del self._data[merchant_id]



class SQLiteStore:
    def __init__(self, db_path: str = "merchants.db") -> None:
        self.db_path = db_path
        self._setup()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _setup(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS merchants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT
                )
                """
            )

    def list(self) -> List[MerchantOut]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, name, description FROM merchants ORDER BY id"
            ).fetchall()
        return [MerchantOut(id=row[0], name=row[1], description=row[2]) for row in rows]


    def get(self, merchant_id: int) -> MerchantOut:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, name, description FROM merchants WHERE id = ?",
                (merchant_id,),
            ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Merchant not found")
        return MerchantOut(id=row[0], name=row[1], description=row[2])

    def create(self, payload: MerchantCreate) -> MerchantOut:
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO merchants (name, description) VALUES (?, ?)",
                (payload.name, payload.description),
            )
            merchant_id = cursor.lastrowid
        return MerchantOut(id=merchant_id, **payload.dict())

    def update(self, merchant_id: int, payload: MerchantUpdate) -> MerchantOut:
        with self._connect() as conn:
            cursor = conn.execute(
                "UPDATE merchants SET name = ?, description = ? WHERE id = ?",
                (payload.name, payload.description, merchant_id),
            )
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Merchant not found")
        return MerchantOut(id=merchant_id, **payload.dict())

    def delete(self, merchant_id: int) -> None:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM merchants WHERE id = ?", (merchant_id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Merchant not found")


