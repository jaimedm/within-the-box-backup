from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from decimal import Decimal
from logic.new_pipeline import set_generation_pipeline
from models import product_related_models
from schemas import productset_schema, product_schema
from dependencies import database_dependencies
from copy import deepcopy

router = APIRouter()

import datetime

# NOTE: Since it is not possible to send body data on the client side, 
# making this a "POST" method was the solution. Otherwise, if 
# productset_schema.Configuration would ever change, this endpoint would 
# also have to change. Besides, passing the configurations as query 
# parameters, would be complicated for the layout, for instance, because
# it is a list (Applicable only for the PREVIOUS VERSION).
@router.post("/get-product-sets/", response_model=list[productset_schema.ProductSet])
async def get_product_sets(configuration: productset_schema.Configuration, db: Session=Depends(database_dependencies.get_db)) -> list[productset_schema.ProductSet]:
    # Configuration validation (in case something does not work on the frontend)
    if configs_validation(configuration.container_dimensions, configuration.n) == False:
        raise HTTPException(status_code=500, detail="Invalid data!")

    # Create a copy and convert configurations if the measurements are expressed in units other than 'cm'
    if configuration.unit != "cm":
        normalized_configuration = convert_configurations(configuration)

    # Fetching all the data
    all_products = db.query(product_related_models.Product).all()

    # Set generation
    generated_sets = set_generation_pipeline(all_products, configuration.container_dimensions, configuration.n, configuration.container_type)
    # NOTE: this is relative to the previous version
    #generated_sets = set_generation_pipeline(all_products, configuration.layout, configuration.container_dimensions)

    # Formating the returned information and associating the original configurations
    list_set_objects = set_formatter(generated_sets, configuration)

    return list_set_objects

# Function to convert the list of generated sets into a list of ProductSet objects to be shown on the frontend
def set_formatter(generated_sets, configuration) -> list[productset_schema.ProductSet]:
    list_set_objects = []
    # Iterate over all sets
    for st in generated_sets:
        product_list = []
        # Iterate through a set
        for idx in st["product_set"]:
            product = product_schema.Product.parse_obj(idx)
            product_list.append(product)
        product_set = productset_schema.ProductSet(timestamp=datetime.datetime.now(), wasted_volume_fraction=st["wasted_volume"], product_list=product_list, configuration=configuration)
        list_set_objects.append(product_set)

    return list_set_objects

# Function used to convert measurements expressed in other units to SI. 
# It returns an object of converted configurations to be sent to the generator
def convert_configurations(configuration) -> productset_schema.Configuration:
    # Inch to Centimetre
    if configuration.unit == "in":
        convertion_factor = Decimal(2.54)

    # TODO: other units
    if configuration.unit == "m":
        pass

    normalized_configuration = deepcopy(configuration)
    normalized_configuration.unit = "cm"
    normalized_configuration.container_dimensions = [value * convertion_factor for value in normalized_configuration.container_dimensions]

    return normalized_configuration

# Function that verifies if a certain number of boxes, along an axis, is within the acceptable range
def box_number_validation(box_number, max) -> bool:
    if box_number >= 1 and box_number <= max:
        return True
    return False

# NOTE: this is relative to the previous version
# Function to validate layout-related inputs
# def layout_validation(layout, n, max_per_axis, max_total) -> bool:
#     if n <= max_total and \
#         box_number_validation(layout[0], max_per_axis) and \
#         box_number_validation(layout[1], max_per_axis) and \
#         box_number_validation(layout[2], max_per_axis):
#         return True
#     return False

# Function used to check if a given dimension is witin the allowed values
def dimension_validation(dim, max) -> bool:
    if dim > 0 and dim <= max:
        return True
    return False

# Function to validate the volume-related inputs
def volume_validation(dims, max_per_axis, max_volume) -> bool:
    if dims[0] * dims[1] * dims[2] <= max_volume and \
        dimension_validation(dims[0], max_per_axis) and \
        dimension_validation(dims[1], max_per_axis) and \
        dimension_validation(dims[2], max_per_axis):
      return True
    return False

# Main function to validate the configurations
def configs_validation(dimensions, n) -> bool:
    # NOTE: this is relative to the previous version
    # return layout_validation(layout, n, 10, 10) and volume_validation(dimensions, 150, 1000000)

    return box_number_validation(n, 10) and volume_validation(dimensions, 150, 1000000)