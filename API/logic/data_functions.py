import pandas as pd

# Function to update the dimensions of the products (if it does not have a lid, its height matches the containers')
def update_dimensions(product_table, container) -> pd.DataFrame:
    for product in product_table.itertuples():
        if product.lidded == False:
                product_table.loc[product.Index, 'height'] = container[2]
    return product_table

# Function to filter de dataframe according to a container's dimensions
def filter_by_dimensions(product_table, container) -> pd.DataFrame:
    if not product_table.empty:
        #simple filtering (not alternating width and depth)
        #return product_table.loc[(product_table['Width'] <= float(container[0])) & (product_table['Depth'] <= float(container[1])) & (product_table['Height'] <= float(container[2]))]

        #filtering by switching width and depth
        return product_table.loc[((product_table['length'] <= float(container[0])) & (product_table['width'] <= float(container[1])) | 
                                    (product_table['width'] <= float(container[0])) & (product_table['length'] <= float(container[1])))
                                & (product_table['height'] <= float(container[2]))]
    else:
        return pd.DataFrame()