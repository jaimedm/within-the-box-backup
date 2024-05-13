from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings

from database.database import engine
from models import product_related_models
from routes import products, sets

# Useful commands
#pg_ctl -D /usr/local/var/postgres start
#uvicorn main:app --reload

# create database tables (consider deleting it in production)
product_related_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME, 
              version=settings.PROJECT_VERSION)

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    # Cross-Origin Resource Sharing (CORS)
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(sets.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


#------------------------------------------------------------------------------------------------------------------------------------
#APAGAR IMPORTAÇÕES NÃO UTILIZADAS
# Example to delete

# @app.get("/files/{file_path:path}")
# async def read_file(file_path: str):
#     return {"file_path": file_path}

# @app.get("/test/{item}")
# async def read_item(item: int):
#     return {"item": item}

# @app.get("/items/")
# async def read_item2(n1: int = 0, n2: int = 10, z : bool = False):
#     if z:
#         return n1 * n2
#     else:
#         return -1
    
# @app.get("/users/{user}/item/{item_id}")
# async def read_item3(user: str, item_id: int, desc: str, n: int=None):
#     item = {"item_id": item_id, "owner_id": user, "description": desc}
#     if n:
#         item.update({"quantity": n})
#     return item


# db = []

# class Item(BaseModel):
#     name: str
#     description: str = "boas"
#     price: float

# @app.post("/postitems/")
# async def create_item(item: Item):
#     db.append(item)
#     return 200

# @app.get("/getitems/")
# async def get_item():
#     return db

#------------------------------------------------------------------------------------------------------------------------------------
