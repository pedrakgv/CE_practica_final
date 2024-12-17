import random
import numpy as np

"""Modulo de operadores de cruce"""

def uniformCrossOver(parents: list):
    if len(parents) != 2:
        raise ValueError
    parent1= parents[0]
    parent2 = parents[1]

    child1 = []
    child2 = []

    mask = [random.randint(0, 1) for _ in range(len(parent1))]
    for i in range(len(parent1)):
        if mask[i] == 0:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])

    return child1, child2

def plainCrossOver(parents: list):
    if len(parents) != 2:
        raise ValueError
    parent1= parents[0]
    parent2 = parents[1]

    child1 = []
    child2 = []

    for i in range(len(parent1)):
        # Definir el rango basado en los valores de los padres
        min_value = min(parent1[i], parent2[i])
        max_value = max(parent1[i], parent2[i])

        # Generar valores aleatorios dentro del rango
        random_value1 = random.uniform(min_value, max_value)
        random_value2 = random.uniform(min_value, max_value)

        child1.append(random_value1)
        child2.append(random_value2)

    return child1, child2


def combinedCrossOver(parents: list, alpha=0.5):
    """
    Cruce combinado (BLX-alpha)
    :param
    - parents: lista de cadenas de genes de dos padres
    - alpha: valor que controla intervalo de cruce

    return: 
    - child1: cromosoma Hijo1
    - child2: cromosoma Hijo2
    """

    parent1= parents[0]
    parent2 = parents[1]

    # incializamos los hijos
    child1 = []
    child2 = []

    # Generar hijos
    for i in range(len(parent1)):  # recorremos genes de los padres
        # calcular límites del intervalo de cruce
        I = abs(parent1[i] - parent2[i])
        min_value = min(parent1[i], parent2[i] - alpha * I)
        max_value = max(parent1[i], parent2[i] + alpha * I)

        # Gen i del Hijo 1
        child1_value = random.uniform(min_value, max_value)
        child1.append(child1_value)

        # Gen i para Hijo 2
        child2_value = min_value + max_value - child1_value
        child2.append(child2_value)

    return child1, child2


def morphologicalCrossOver(parents: list):
    # normalizamos los padres
    parents_norm = []
    for parent in parents:
        minimo = min(parent)
        maximo = max(parent)
        if maximo != minimo:
            parent_norm = [(value - minimo) / (maximo - minimo) for value in parent]
        else:
            parent_norm = [0] * len(parent)  # Normalizar a 0 si todos los valores son iguales
        parents_norm.append(parent_norm)
    
    # función de exploración - explotación
    def phi(gi, a=-0.001, b=-0.133, c=0.54, d=0.226):
        if gi <= c:
            m = (b - a) / c
            return m * gi + a
        else:
            m = (d - 0) / (1 - c)
            return m * (gi - c) + 0

    matrixG = np.array(parents_norm)  # matriz G 
    _, colums = matrixG.shape

    child1 = []
    child2 = []

    for i in range(colums):
        fi = matrixG[:,i]
        # cálculo de medida de diversidad
        gi = fi.max() - fi.min()

        # cálculo de intervalo de cruce
        gi_min = min(fi) + phi(gi)
        gi_max = max(fi) - phi(gi)

        # cálculo de descendencia
        child1_value = random.uniform(gi_min, gi_max)
        child1.append(child1_value)

        child2_value = gi_min + gi_max - child1_value
        child2.append(child2_value)
        
    return child1, child2



# -----------------------------------------------------------------------------------------------------

def uniformCrossOverWeights(parent1, parent2, child1, child2): #Given two parent car objects, it modifies the children car objects weights
    sizenn = len(child1.sizes) #3 si car1=Car([2, 4, 3])
    
    #Copy parent weights into child weights
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]
                
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child2.weights[i][j][k] = parent2.weights[i][j][k]
                
    #Copy parent biases into child biases
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
                child1.biases[i][j] = parent1.biases[i][j]
                
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
                child2.biases[i][j] = parent2.biases[i][j]

    genome1 = [] #This will be a list containing all weights of child1
    genome2 = [] #This will be a list containing all weights of child2
        
    for i in range(sizenn-1): #i=0,1
        for j in range(child1.sizes[i]*child1.sizes[i+1]):
            genome1.append(child1.weights[i].item(j))
            
    for i in range(sizenn-1): #i=0,1
        for j in range(child2.sizes[i]*child2.sizes[i+1]):
            genome2.append(child2.weights[i].item(j))

    #Crossover weights          
    alter = True    
    for i in range(len(genome1)):
        if alter == True:
            aux = genome1[i]
            genome1[i] = genome2[i]
            genome2[i] = aux
            alter = False
        else:
            alter = True

    #Go back from genome list to weights numpy array on child object
    count = 0
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = genome1[count]
                count += 1
          
    count = 0
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
            for k in range(child2.sizes[i]):
                child2.weights[i][j][k] = genome2[count]
                count += 1              
    return 


def uniformCrossOverBiases(parent1, parent2, child1, child2): #Given two parent car objects, it modifies the children car objects biases
    sizenn = len(parent1.sizes)
    
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]
                
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child2.weights[i][j][k] = parent2.weights[i][j][k]
                
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
                child1.biases[i][j] = parent1.biases[i][j]
                
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
                child2.biases[i][j] = parent2.biases[i][j]
                
    genome1 = []
    genome2 = []
    
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            genome1.append(child1.biases[i].item(j))
            
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
            genome2.append(child2.biases[i].item(j))
     
    alter = True    
    for i in range(len(genome1)):
        if alter == True:
            aux = genome1[i]
            genome1[i] = genome2[i]
            genome2[i] = aux
            alter = False
        else:
            alter = True
    
    count = 0    
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
                child1.biases[i][j] = genome1[count]
                count += 1
                
    count = 0    
    for i in range(sizenn-1):
        for j in range(child2.sizes[i+1]):
                child2.biases[i][j] = genome2[count]
                count += 1
    return 