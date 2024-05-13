from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import product_related_models
from schemas import product_schema
from dependencies import database_dependencies

router = APIRouter()

#------------------------------------------------------------------------------------------------------------------------------------
# Example to delete
@router.post("/userstab", response_model=product_schema.User)
async def create_user(usr: dict, db: Session = Depends(database_dependencies.get_db)):
    user = product_related_models.UserForTab1(**usr)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Test methodss for the database
@router.post("/postproduct")
async def create_product(product: dict, db: Session=Depends(database_dependencies.get_db)):
    product = product_related_models.Product(**product)
    db.add(product)
    db.commit()
    db.refresh(product)
    return {"message": "User Created!"}

@router.get("/getproduct/{id}", response_model=product_schema.Product)
async def get_product_by_id(id: str, db: Session=Depends(database_dependencies.get_db)):
    return db.query(product_related_models.Product).filter(product_related_models.Product.id == id).first()

#------------------------------------------------------------------------------------------------------------------------------------

@router.get("/get-products-by-index/", response_model=list[product_schema.Product])
async def get_products(begin: int, end: int, db: Session=Depends(database_dependencies.get_db)) -> list[product_schema.Product]:
    # Raises an exception if the inferior limit is greater than superior limit
    if end < begin:
        raise HTTPException(status_code=500, detail="The lower bound cannot be greater than the upper bound!")
    
    # Get table size
    table_size = db.query(product_related_models.Product).count()
    # Last index: table_size-1
    if begin > table_size - 1:
        return []

    # Not needed
    if end > table_size:
        end = table_size

    # Querying an interval of products (includes the two interval extremes)
    return db.query(product_related_models.Product).offset(begin).limit(end - begin + 1).all()