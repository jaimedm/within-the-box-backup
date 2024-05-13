from pydantic import BaseModel, Field, validator, HttpUrl
from uuid import UUID
from decimal import Decimal

#------------------------------------------------------------------------------------------------------------------------------------
# MUDAR O NOME DO FICHEIRO 
# Example to delete
class User(BaseModel):
    name: str
    age: int
    active: bool

    class Config:
        orm_mode = True

#------------------------------------------------------------------------------------------------------------------------------------

# Product schema
class Product(BaseModel):
    # E.g. x: str = Field(...) --> here a "Field" object is 
    # assigned to a field named "x" of type "str".

    # Here, since id is generated automatically, 
    # one cannot manually provide it, upon the object's 
    # creation. Therefore, id is an UUID with default
    # value None. To complement the validation,
    # a validator was added on the model side.
    id: UUID = Field(description="Product's unique identifier", default=None)
    name : str = Field(description="Product's name", max_length=25)
    url : HttpUrl = Field(description="URL to the product's page on the seller's website")
    image_source: HttpUrl = Field(description="URL of the product's image")
    description : str | None = Field(description="Small text describing the product", max_length=50, default=None)
    length : Decimal = Field(description="Product's length in cm", decimal_places=3)
    width : Decimal = Field(description="Product's width in cm", decimal_places=3)
    height : Decimal = Field(description="Product's height in cm", decimal_places=3)
    weight : Decimal = Field(description="Product's weight in kg", decimal_places=3)
    lidded : bool = Field(description="Indicates whether the product has a lid or not", default=False)
    price : Decimal = Field(description="Product's price", decimal_places=3)
    currency : str = Field(description="Currency associated with the product's price", max_length=5)
    materials : list[str] = Field(description="Materials that constitute the product", max_length=15, default=None)
    brand : str | None = Field(description="Product's seller/manufacturer", max_length=15, default=None)

    class Config:
        orm_mode = True