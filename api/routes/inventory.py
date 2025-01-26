from fastapi import APIRouter, HTTPException
from db.db_connection import get_db_connection

router = APIRouter()

@router.get("/items")
def get_items():
    return {"message": "Inventory items endpoint"}

@router.get("/restocking_matrix")
def get_restocking_matrix():
    connection = get_db_connection()
    query = "SELECT * FROM restocking_matrix"
    result = connection.execute(query).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No data found")
    return {"data": [dict(row) for row in result]}