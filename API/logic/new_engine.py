import pandas as pd
from copy import deepcopy

#--------------------------------------------------
# BOX SPACE FUNCTIONS
# Function to update the list of combinations
def update_list(lst, total_lst) -> list(dict()):
    for comb in lst:
        # checking if the combination has not already been added
        if comb not in total_lst:
            total_lst.append(comb)
    return total_lst

# Function to create the box space universe based on dimensions and number of boxes
def box_space_universe(x, y, n) -> dict:
    factor = 1
    count = 0
    U = {}
    while factor < n+1:
        if n % factor == 0:
            #--------------------------------------------------
            # debug:
            # To help debugging the algorithm, one can work just with fractions 
            #of a container (E.g. 1/8th of the length) instead of real dimensions.
            #U[count] = [factor, (n/factor)]
            #--------------------------------------------------
            U[count] = [float(x)/factor, float(y)/(n/factor)]
            count += 1
        factor += 1
    return U

# Function that creates a mapping between the box spaces of a given universe
def get_mapping(U) -> dict:
    num_divisions = len(U)
    mapping = {}
    for idx in range(num_divisions-1):
        if idx not in mapping.keys():
            mapping[idx] = {}
        for i in range(idx+1, num_divisions):
            mapping[idx][i] = [a / b for a , b in zip(U[idx], U[i])]
            if i not in mapping.keys():
                mapping[i] = {}
            mapping[i][idx] = [b / a for a , b in zip(U[idx], U[i])]

    return mapping

# Function to generate new combinations    
def combination_factory(combination, mapping, num_divisions) -> list(dict()):
    new_combs_lst = []
    # For each box space available
    for elem in mapping.keys():
        # For each box space mapped to a given box space 
        #(elem, elem_comb) forms a mapping that translates into a relationship between two box spaces
        for elem_comb in mapping[elem].keys():
            # Factor representing the number of box spaces replaced, considering a pair (elem, elem_comb)
            #(subtracted to a given elem box space and added to a box space elem_comb that has a mapped relationship with elem
            factor = int(mapping[elem][elem_comb][1]) if mapping[elem][elem_comb][1] >= 1 else int(mapping[elem][elem_comb][0])
            # Condition to make sure that, after the creation of a new combination, 
            #the number of each box space in the new combination is always greater or equal than zero
            if combination[elem] >= factor:
                new_comb = deepcopy(combination)
                new_comb[elem] -= factor
                new_comb[elem_comb] += factor
 
                # Block to evaluate whether the new combination is valid
                able = True
                # For every box space i mapped to a given box space that is present in the combination being analysed 
                for i in mapping[elem].keys():
                    # If the box space is part of the combination
                    if new_comb[i] > 0:
                        # Makes sure that we are only checking those conditions for two different box spaces
                        if i != elem:
                            # Box spaces that cover all length/height cannot be combined with others that cover all height/lenght
                            if new_comb[elem] > 0 and (mapping[elem][i][0] == num_divisions or mapping[elem][i][1] == num_divisions):
                                able = False
                                break
                            '''if factor % (new_comb[i]/new_comb[elem_comb]) != 0 and factor % (new_comb[elem_comb]/new_comb[i]) != 0:
                                able = False
                                break'''
                        # This has to be done both for elem and elem_comb, since we are removing and adding from them, 
                        #so the resulting combination remains valid
                        if i != elem_comb:
                            # NOTE: new_comb[elem_comb] is always > 0 since we add the factor
                            if (mapping[elem_comb][i][0] == num_divisions or mapping[elem_comb][i][1] == num_divisions):
                                able = False
                                break
                            # NOTE: not sure if this can be done this way. I works because the values are equal, but the logic may not be correct
                            # The calculated factor (relationship between elem and elem_comb present in the mapping record)
                            #has to be divisible by the ratio of the number of a given box space to
                            #the updated number of box space elem_comb in the new combination or vice-versa,
                            #i.e. the number of replaced box spaces (added in elem_comb) needs to be in accordance 
                            #to the new ratio of a given box to the updated one (elem_comb)
                            '''if factor % (new_comb[i]/new_comb[elem_comb]) != 0 and factor % (new_comb[elem_comb]/new_comb[i]) != 0:
                                able = False
                                break'''
                            # The number of box spaces set in the mapping of two box spaces (a given box space and the updated one elem_comb)
                            #needs to be in accordance to the new ratio of a given box to the updated one (elem_comb). I.e when there is a 
                            #switch between two box spaces, the ratio should be, not only valid for the two switched box spaces, but also
                            #for the other box spaces in the combination.
                            if  mapping[elem_comb][i][0] % (new_comb[i]/new_comb[elem_comb]) != 0 and mapping[elem_comb][i][1] % (new_comb[elem_comb]/new_comb[i]) != 0:
                                able = False
                                break
                # Adds the new combination to the list if all conditions were met
                if able:
                    new_combs_lst.append(new_comb)

    return new_combs_lst

# Function that calls the factory, adds the new combinations to the list and decides when to stop generating
def factory_master(combinations, mapping, num_divisions) -> list(dict()):
    combination_lst = []
 
    more = True
    while more:
        count = 0
        # For every newly generated combinations it checks if it had already been generated 
        #and adds it to the list, if not
        for c in combinations:
            if c not in combination_lst:
                combination_lst.append(deepcopy(c))
                count += 1
 
        # When no more combinations were found, it stops generating new ones
        if count == 0:
            more = False
        else:
            for comb in combinations:
                combinations = combination_factory(deepcopy(comb), mapping, num_divisions)
 
    return combination_lst

#--------------------------------------------------
# debug:
# Auxiliar function to print a combination list in a more readable format
#(E.g. {0: 0, 1: 2, 2: 2, 3: 4} -> 11223333)
def print_list(lst):
    for comb in lst:
        st = ""
        for k in comb.keys():
            st += str(k) * comb[k]
        print(st)
#--------------------------------------------------

# Function that sequentially executes all program steps
# NOTE: A box space is the maximum dimensions a box shall have to fit in a given combination
def space_generation_pipeline(container_dimensions, num_divisions) -> tuple:
    total_comb_lst = []
 
    # Dividing the space into box spaces
    U = box_space_universe(container_dimensions[0], container_dimensions[1], num_divisions)
    # Calculating the relationship between box spaces
    mapping = get_mapping(U)
 
    num_boxes = len(U)
 
    total_comb_lst = []
    # Creating a number (num_boxes) of initial combinations from which the generation
    #of new combinations starts (E.g. 00000000; 11111111; 22222222; 33333333)
    for comb_n in range(num_boxes):
        init_comb = {}
        for box_n in range(num_boxes):
 
            if box_n == comb_n:
                init_comb[box_n] = num_divisions
            else:
                init_comb[box_n] = 0
 
        init_comb_lst = [init_comb]
        # Getting the generated combinations from the initial combination and 
        #appending them to the list, removing the duplicates
        total_comb_lst = update_list(factory_master(init_comb_lst, mapping, num_divisions), total_comb_lst)
 
    #--------------------------------------------------
    # debug:
    # Printing result
    #print_list(total_comb_lst)
    #--------------------------------------------------

    # The function returns the list of calculated box spaces and their dimensions
    return total_comb_lst, U
#--------------------------------------------------

#--------------------------------------------------
# BOX SET FUNCTIONS

# Not implemented
def area() -> float:
    pass

# Not implemented
def wasted_area() -> float:
    pass

# Function to calculate de volume of a box space or product
def volume(dimensions) -> float:
    return float(dimensions[0]) * float(dimensions[1]) * float(dimensions[2])

# Function to calculate the wasted volume of the product in relation to a box space
def wasted_volume(space_dimensions, product_dimensions) -> float:
    return round((volume(space_dimensions) - volume(product_dimensions)) / volume(space_dimensions), 3)

# Function for mapping the box spaces and the products that fit in them
def product_space_mapper(product_table, box_space_universe, container, second_dimension) -> dict:
    # Creates a new mapping dictionary with all box spaces 
    #(E.g. {0: [{product_id: 24fwefs, wasted_space: 0.3}]}) # NOTE: example for product id
    #(E.g. {0: [{product: Dataframe, wasted_space: 0.3}]})
    product_space_mapping = {}
    for box_space in box_space_universe.keys():
        product_space_mapping[box_space] = []

    # For every product in the filtered table
    #for product in product_table.itertuples(): # NOTE: ideal when choosing to work with product id instead of whole product
    for idx in range(len(product_table)):
        product = product_table.iloc[idx]
        # For every box space
        for box_space in box_space_universe.keys():
            # If the product's two most important dimensions fit the box space, it is added to the mapping
            # Method getattr gets an object's attribute. It is used in this case because, 
            #depending on the type of container, one (height or width) of the dimensions considered differs
            if product.length <= box_space_universe[box_space][0] and getattr(product, second_dimension) <= box_space_universe[box_space][1]:
                # Dimensions of a 3D box space
                if second_dimension == "height":
                    space_dimensions = [box_space_universe[box_space][0], container[1], box_space_universe[box_space][1]]
                elif second_dimension == "width":
                    space_dimensions = [box_space_universe[box_space][0], box_space_universe[box_space][1], container[2]]

                # Product's dimensions
                product_dimensions = [product.length, product.width, product.height]

                # Adding the product and fraction of volume that it is not occupied by the product
                product_space_mapping[box_space].append(
                    {
                        #"product_id": product.id, # NOTE: use product id for a more compact set
                        "product": product,
                        "wasted_volume": wasted_volume(space_dimensions, product_dimensions)
                    }
                )

    return product_space_mapping

# Function to calculate the percentage of wasted volume when a new product is added
def update_wasted_volume(old_percentage, product_space_wasted_percentage, num) -> float:
    # Relative to the products already in the set
    old_used_percentage = 1 - old_percentage

    # Relative to the new added product
    new_product_wasted_percentage = product_space_wasted_percentage * (1/num) + ((num-1)/num)
    new_product_used_percentage = 1 - new_product_wasted_percentage

    return round((1 - (old_used_percentage + new_product_used_percentage)), 3)

# Function to update the product sets (for a box space set) with new products
def update_product_sets(possible_box_sets, space, product_space_mapping, num) -> list(dict()):
    updated_possible_box_sets = []

    # For all sets already in the list of possible (incomplete) product sets
    for box_set in possible_box_sets:
        # For each one of the products that fit into that box space
        for product in product_space_mapping[space]:
            new_box_set = deepcopy(box_set)

            # Adds the new products to the set,
            #according to the number of products specified in the box space set
            for _ in range(num):
                new_box_set["wasted_volume"] = update_wasted_volume(new_box_set["wasted_volume"], product["wasted_volume"], num)
                #new_box_set["product_set"].append(product["product"]) # NOTE: when opting for product id 
                new_box_set["product_set"].append(product["product"])
                
            updated_possible_box_sets.append(new_box_set)

    possible_box_sets = updated_possible_box_sets

    return possible_box_sets

# Function which creates sets of products based on the box space sets created earlier
def box_space_sets_to_product_sets(box_space_sets, product_space_mapping) -> list(dict()):
    product_sets = []

    # For all box space sets 
    for space_set in box_space_sets:
        possible_box_sets = [
            {
                "wasted_volume": 1, 
                "product_set": []
            }
        ]
        
        # For each box space in a box space set
        for space, num in space_set.items():
            # se houver espacos desse tipo e produtos
            # If there are box spaces of a certain type in that box space set
            if num > 0:
                # Additionally, it is important to check 
                #if there are products that fit that box space set
                if len(product_space_mapping[space]) > 0:
                    #new_possible_box_sets = []
                    possible_box_sets = update_product_sets(possible_box_sets, space, product_space_mapping, num)

                # If there are no products which can be put in that box space set, 
                #it becomes impossible to form product sets for that box space set
                else:
                    possible_box_sets = []
                    break

        # Updating the list of all possible product sets
        for box_set in possible_box_sets:
            product_sets.append(box_set)

    return product_sets
#--------------------------------------------------

# Function for the engine pipeline:
    # Check container type
    # Call box space generator that creates the combinations of spaces that compose a container
    # Map generated box spaces to real products on the database
    # Create the final sets with those products
    # Select the best sets to return
def sets_engine(product_table, n, container, container_type) -> list(dict()):
    # Reducing dimensionality: 3D to 2D according to the type of container. 
    #For shelfs stacking is preferred while filling in depth is more important when it comes to drawers
    if container_type == "shelf":
        # Length and height
        container_2d = [container[0], container[2]]
        chosen_second_dimension = "height"
    elif container_type == "drawer":
        # Length and width
        container_2d = [container[0], container[1]]
        chosen_second_dimension = "width"
    # Just to avoid different unexpected values
    else:
        raise ValueError("Invalid container type!")
    
    # Box spaces representing different ways of dividing the container
    box_space_sets, box_space_universe = space_generation_pipeline(container_2d, n)

    # Associating the box space type to the products
    product_space_mapping = product_space_mapper(product_table, box_space_universe, container, chosen_second_dimension)

    # Assembling the product sets
    product_sets = box_space_sets_to_product_sets(box_space_sets, product_space_mapping)

    # Ranking the sets based on wasted volume volume (the less waste, the better)
    ranked_product_sets = sorted(product_sets, key=lambda s: s["wasted_volume"])

    # Selecting the top 3 product sets
    #top3_product_sets = ranked_product_sets[:3]
    top3_product_sets = ranked_product_sets

    return top3_product_sets