from pydantic import BaseModel, Field, root_validator
from uuid import UUID, uuid4
from decimal import Decimal
from datetime import datetime
from .product_schema import Product

# Schema for the used filters
class Filter(BaseModel):
    pass
    class Config:
            orm_mode = True

# Schema of configurations used for set calculation
class Configuration(BaseModel):
    n: int = Field(description="Number of products in the set")
    container_dimensions: list[Decimal] = Field(description="Internal dimensions of the products' container", decimal_places=3, min_items=3, max_items=3)
    unit: str = Field(description="Unit in which the container is measured", default="cm")
    filters : Filter | None = Field(description="Other parameters used to filter products during set calculation", default=None)
    # NOTE: this is relative to the current version
    container_type: str = Field(description="Type of container", default="shelf")
    # NOTE: this is relative to the previous version
    #layout: list[int] = Field(description="Products' arrangement across three dimensions", min_items=3, max_items=3)

    # Validator for the measurement unit.
    # Validator for the number of products. The number of 
    # products and their respective layout must be consistent (Applicable only for the PREVIOUS VERSION).
    # Validator for the container type (Applicable only for the CURRENT VERSION).
    # (The root validator validates the entire model after all attributes are filled in)
    @root_validator()
    @classmethod
    # NOTE: this (method name) is relative to the previous version
    #def check_correspondence_n_layout(cls, values: dict) -> dict:
    def check_unit_n_type(cls, values: dict) -> dict:
        if values.get("unit") != "cm" and values.get("unit") != "in":
            raise ValueError("Invalid unit!")
        if values.get("n") < 0:
            raise ValueError("Number of products can't be negative!")
        # NOTE: this is relative to the current version
        if values.get("container_type") != "shelf" and values.get("container_type") != "drawer":
            raise ValueError("Invalid container type!")
        # NOTE: this is relative to the previous version
        # if values.get("n") != values.get("layout")[0] * values.get("layout")[1] * values.get("layout")[2]:
        #     raise ValueError("Number products and their layout are incompatible!") 
        return values


    class Config:
        orm_mode = True

# Schema of the calculated sets
class ProductSet(BaseModel):
    id: UUID = Field(description="Set's unique identifier", default_factory=uuid4)
    timestamp: datetime = Field(description="Date and time when the set was calculated")
    product_list: list[Product] = Field(description="List of products that fit certain configurations and filters")
    wasted_volume_fraction: Decimal = Field(description="Fraction of the container's volume wasted", default=1.0)
    configuration: Configuration = Field(description="Configurations used in set calculation")

    # NOTE: there are situations where the current algorithm outputs sets
        # with different sizes than what was requested
    
    # Validator for the size of the products' list. The
    # size must be consistent with the specified settings.
    # (The root validator validates the entire model after all attributes are filled in)
    # @root_validator
    # @classmethod
    # def check_configured_product_list_size(cls, values: dict) -> dict:
    #     config = values.get("configuration")
    #     if len(values.get("product_list")) != config.n:
    #         raise ValueError(f"Product list must be of length {config.n}!")
    #     else:
    #         return values

    class Config:
        orm_mode = True