"""Modulo de operadores de cruce"""
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