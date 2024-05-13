import pandas as pd
from logic import data_functions
from logic.new_engine import sets_engine

# Function for the set generation pipeline
    # Data pre-processing and filtering
    # Call the engine
def set_generation_pipeline(raw_data, container, n, container_type) -> list(dict()):
    # Converts the raw data into a data frame
    #product_dataframe = pd.DataFrame({"Original index": i, **row.__dict__} for i, row in enumerate(raw_data)) # NOTE: to use when it is important to keep the product's index in the original table
    product_dataframe = pd.DataFrame([row.__dict__ for row in raw_data])

    # Removing boxes with greater height, length and width than the dimensions allowed by the container
    filtered_data = data_functions.filter_by_dimensions(product_dataframe, container)

    # Sets the height to the container's height when a storage box is not lidded
    box_sets = []
    if not filtered_data.empty:
        treated_data = data_functions.update_dimensions(filtered_data, container)
        print(treated_data.iloc[3])

        # Calling the engine
        if not treated_data.empty:
            box_sets = sets_engine(treated_data, n, container, container_type)

    return box_sets
    #--------------------------------------------------
    # debug:
    #return [[0.97, product_dataframe.iloc[3], product_dataframe.iloc[4]], [0.54234, product_dataframe.iloc[0], product_dataframe.iloc[0], product_dataframe.iloc[1]]]
    #--------------------------------------------------