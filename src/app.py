from fastapi import FastAPI, Query
from contextlib import asynccontextmanager

from db.db_adapter import DBAdapter

db_adapter= DBAdapter(db_engine='sqlite')

@asynccontextmanager
async def lifespan(app:FastAPI):
    yield
    await db_adapter.close()
   
app= FastAPI(lifespan=lifespan) 

@app.get("/users")
async def get_user(page: int = Query(1, gt=0), size: int =
Query(10, le=100)):
    return {"page": page, "size": size}

if __name__=='__main__':
    import uvicorn
    uvicorn.run('app:app',reload=True)