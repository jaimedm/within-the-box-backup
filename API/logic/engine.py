import copy
import random
from logic.data_functions import filter_by_dimensions
import pandas as pd

# Function to calculate the volume
def volume(dimensions) -> float:
    return float(dimensions[0]) * float(dimensions[1]) * float(dimensions[2])

#--------------------------------------------------
# GENETIC FUNCTIONS
# Function to confront old generation individuals with the newly generated ones
def elitism(old_generation, child_generation, gen_size) -> list(list()):
    for parent in old_generation:
        if parent not in child_generation:
            child_generation.append(parent)
    child_generation.sort()
    
    child_size = len(child_generation)
    #--------------------------------------------------
    # debug:
    # print(child_size)
    # for st in child_generation:
    #     print(st)
    # print("\n")
    #--------------------------------------------------

    if child_size < gen_size:
        gen_size = child_size

    return child_generation[0:gen_size]

# Function to remove sets with negative wasted volume percentage (bigger than the container)
def remove_negatives(sorted_generation) -> list(list()):
    flag = 0
    i = 0
    while flag != 1 and len(sorted_generation) > 0:
        if sorted_generation[i][0] >= 0:
            flag = 1
        else:
            sorted_generation.pop(i)
            i -= 1
        i += 1
        
    return sorted_generation

# Function to select the best individuals in a generation (percentage of wasted volume between 0 and 0.5)
def selection(generation) -> tuple([list(), list(list())]):
    survivors = []
    if len(generation) > 0:
        best = generation[0]
    else: 
        best = [1]
    for st in generation:
        if st[0] >= 0  and st[0] <= 0.5:
            survivors.append(st)
            if st[0] < best[0]:
                best = st

    return best, survivors

# Function to create, mutate and crossover a generation
def generation_generation(product_table_x, old_generation, volume_x, x_N, gen_size, percent_mut, percent_cross, c_x, layout_x) -> list(list()):
    N = x_N[0]
    if N == 1:
        N = 2
    #TODO: throw exception if all summed percentages are not equal to 1
    #TODO: resolver o problema da ordem dos conjuntos ([..., 9, 25] == [..., 25, 9])

    #Random generations
    for _ in range(int(gen_size-len(old_generation))):
        sol = [1]
        buffer = copy.deepcopy(c_x)
        #NOTE: it needs the flag here, so that the mutation and crossover (after the first generation) 
        # are done over generated solutions that always have the same length. In the mutations and
        #crossovers, the  flag is not needed because the length is not being altered
        flag = 0
        total_volume = 0
        for _ in range(N):
            idx = random.randint(0, len(product_table_x)-1)
            product = product_table_x.iloc[idx]
            buffer[0] -= product.length
            #buffer[1] -= product.width
            #buffer[2] -= product.height
            sol.append(idx)
            #TODO:CUIDADO: ver se a disposicao interessa nestes casos (largura trocada com a profundidade)!
            if buffer[0] >= 0 and buffer[1] >= 0 and buffer[2] >= 0 and flag != -1:
                total_volume += volume([product_table_x.iloc[idx].length, product_table_x.iloc[idx].width, product_table_x.iloc[idx].height])
                #sol[0] = sol[0] * calcWastedVolumePercentage(product_table_x.iloc[idx], volume_x*sol[0])
            else:
                sol[0] = -1
                flag = -1

        if sol[0] >= 0 and flag != -1:
            sol[0] = 1-(total_volume/volume_x)
        old_generation.append(sol)

    #Mutations
    for _ in range(int(gen_size * percent_mut)):
        idx = random.randint(0, len(product_table_x)-1)
        gen_idx = random.randint(0, len(old_generation)-1)
        pos = random.randint(1, N-1)
        chosen_one = old_generation[gen_idx][pos]
        while idx == chosen_one:
            idx = random.randint(0, len(product_table_x)-1)
        #update info
        old_generation[gen_idx][pos] = idx
        old_generation[gen_idx][0] = 1
        buffer = copy.deepcopy(c_x)
        total_volume = 0
        flag = 0
        for n in range(1,N+1):
            product = product_table_x.iloc[old_generation[gen_idx][n]]
            buffer[0] -= product.length
            #buffer[1] -= product.width
            #buffer[2] -= product.height
            if buffer[0] >= 0 and buffer[1] >= 0 and buffer[2] >= 0 and flag != -1:
                total_volume += volume([product.length, product.width, product.height])                                               
                #old_generation[gen_idx][0] = old_generation[gen_idx][0] * calcWastedVolumePercentage(product, 
                #                                                        volume_x*old_generation[gen_idx][0])
            else:
                old_generation[gen_idx][0] = -1
                flag = -1

        if old_generation[gen_idx][0] >= 0 and flag != -1:
            old_generation[gen_idx][0] = 1-(total_volume/volume_x)

    #Crossover
    for _ in range(int(gen_size * percent_cross)):
        gen_idx = random.randint(0, len(old_generation)-1)
        gen_idx2 = random.randint(0, len(old_generation)-1)
        pos = random.randint(1, N-1)
        pos2 = random.randint(1, N-1)
        chosen_one = old_generation[gen_idx][pos]
        chosen_two = old_generation[gen_idx2][pos2]
        #while chosen_one != chosen_two:
            #gen_idx = random.randint(0, len(product_table_x)-1)
        old_generation[gen_idx][pos] = chosen_two
        old_generation[gen_idx][0] = 1
        old_generation[gen_idx2][pos] = chosen_one
        old_generation[gen_idx2][0] = 1
        buffer = copy.deepcopy(c_x)
        buffer2 = copy.deepcopy(c_x)
        total_volume = 0
        total_volume2 = 0
        flag = 0
        flag2 = 0
        for n in range(1,N+1):
            product = product_table_x.iloc[old_generation[gen_idx][n]]
            buffer[0] -= product.length
            #buffer[1] -= product.width
            #buffer[2] -= product.height

            product2 = product_table_x.iloc[old_generation[gen_idx2][n]]
            buffer2[0] -= product2.length
            #buffer2[1] -= product2.width
            #buffer2[2] -= product2.height

            if buffer[0] >= 0 and buffer[1] >= 0 and buffer[2] >= 0 and flag != -1:
                total_volume += volume([product.length, product.width, product.height])
                #old_generation[gen_idx][0] = old_generation[gen_idx][0] * calcWastedVolumePercentage(product, 
                #                                                        volume_x*old_generation[gen_idx][0])
            else:
                old_generation[gen_idx][0] = -1
                flag = -1

            if buffer2[0] >= 0 and buffer2[1] >= 0 and buffer2[2] >= 0 and flag2 != -1:
                total_volume2 += volume([product2.length, product2.width, product2.height])
                #old_generation[gen_idx2][0] = old_generation[gen_idx2][0] * calcWastedVolumePercentage(product2, 
                #                                                        volume_x*old_generation[gen_idx2][0])
            else:
                old_generation[gen_idx2][0] = -1
                flag2 = -1

        if old_generation[gen_idx][0] >= 0 and flag != -1:
            old_generation[gen_idx][0] = 1-(total_volume/volume_x)
        if old_generation[gen_idx2][0] >= 0 and flag2 != -1:
            old_generation[gen_idx2][0] = 1-(total_volume2/volume_x)
        
    return old_generation

# Function for the genetic algorithm
def genetic_build(product_table_x, volume_x, x_N, c_x, layout_x) -> list(list()):
    gen_size = 300
    limit_same_best = 5

    old_generation = generation_generation(product_table_x, [], volume_x, x_N, gen_size, 0, 0, c_x, layout_x)
    old_generation.sort()
    old_generation = remove_negatives(old_generation)

    child_generation = []
    
    count_best = 0
    old_best = [1]
    while count_best < limit_same_best:
        if len(old_generation) > 0:
            old_best = old_generation[0]

        child_generation = generation_generation(product_table_x, old_generation, volume_x, x_N, gen_size, 0.4, 0.3, c_x, layout_x)
        child_generation.sort()
        child_generation = remove_negatives(child_generation)
        best, old_generation = selection(old_generation)
        old_generation = elitism(old_generation, child_generation, gen_size)

        if old_best[0] <= best[0]:
            count_best += 1
        else:
            count_best = 0

   #--------------------------------------------------
    # debug:
    # print(len(old_generation))
    # for st in old_generation:
    #     print(st)
    #--------------------------------------------------

    #x% sao mudados ou mutados
    #100-x% sao randomizados
    #ver quais passam para a seguinte

    return old_generation
#--------------------------------------------------



# Function for the set generator pipeline
    # Filtering by subcontainer
    # Call genetic algorithm
    # result processing
def generate_sets(product_table, x_N, c_x, layout_x) -> list(list()):
    # Filtering table by subcontainer
    volume_x = volume(c_x)
    product_table_x = filter_by_dimensions(product_table, c_x)
    product_table_x = product_table_x.reset_index(drop=True)

    # If the table is not empty, calls the function to build the sets
    box_sets_x = []
    if not product_table_x.empty:
        box_sets_x = genetic_build(product_table_x, volume_x, x_N, c_x, layout_x)
    
    # Replacing de transformed table's indeces by the original table's entry
    for st in box_sets_x:
        for idx in range(1, len(st)):
            original_idx = product_table_x.iloc[st[idx]]["Original index"]
            st[idx] = product_table.iloc[original_idx]

    return box_sets_x

# Function for the engine pipeline
    # Split by dimension
    # Call set generator
def sets_engine(product_table, layout, container) -> list(list()):
    # [number of boxes per set, number of equal sets needed to fill the space]
    l_N = [layout[0], layout[1] * layout[2]]
    w_N = [layout[1], layout[0] * layout[2]]
    h_N = [layout[2], layout[0] * layout[1]]

    #--------------------------------------------------
    # debug:

    #NOTE: ele está a adicionar conjuntos iguais: quando o conjunto termina, ele tem de verificar se aquele conjunto já tinha sido feito
    #NOTE: limite de execuções? recursivo ou nao 

    # Generate sets by dimension

    # Length subcontainer sets
    c_l = [container[0], container[1]/layout[1], container[2]/layout[2]]
    layout_l = [layout[0], 1, 1]
    box_sets_l = generate_sets(product_table, l_N, c_l, layout_l)

    # Width subcontainer sets
    c_w = [container[0]/layout[0], container[1], container[2]/layout[2]]
    layout_w = [1, layout[1], 1]
    box_sets_w = generate_sets(product_table, w_N, c_w, layout_w)

    # Height subcontainer sets
    c_h = [container[0]/layout[0], container[1]/layout[1], container[2]]
    layout_h = [1, 1, layout[2]]
    box_sets_h = generate_sets(product_table, h_N, c_h, layout_h)
    #--------------------------------------------------

    return box_sets_l + box_sets_w + box_sets_h