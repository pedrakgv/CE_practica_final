"""Modulo de operadores de mutacion"""

import random

def mutateOneWeightGene(parent1, child1):
    sizenn = len(child1.sizes)
    
    #Copy parent weights into child weights
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]          
                
    #Copy parent biases into child biases
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
                child1.biases[i][j] = parent1.biases[i][j]

    genomeWeights = [] #This will be a list containing all weights, easier to modify this way
    
    for i in range(sizenn-1): #i=0,1
        for j in range(child1.sizes[i]*child1.sizes[i+1]):
            genomeWeights.append(child1.weights[i].item(j))
    
    #Modify a random gene by a random amount
    r1 = random.randint(0, len(genomeWeights)-1)
    genomeWeights[r1] = genomeWeights[r1]*random.uniform(0.8, 1.2)
    
    count = 0
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = genomeWeights[count]
                count += 1
    return


def mutateOneBiasesGene(parent1, child1):
    sizenn = len(child1.sizes)
    

    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            for k in range(child1.sizes[i]):
                child1.weights[i][j][k] = parent1.weights[i][j][k]          
                
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
                child1.biases[i][j] = parent1.biases[i][j]

    genomeBiases = []
    
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
            genomeBiases.append(child1.biases[i].item(j))
            
    r1 = random.randint(0, len(genomeBiases)-1)
    genomeBiases[r1] = genomeBiases[r1]*random.uniform(0.8, 1.2)
    
    count = 0    
    for i in range(sizenn-1):
        for j in range(child1.sizes[i+1]):
                child1.biases[i][j] = genomeBiases[count]
                count += 1
    return
