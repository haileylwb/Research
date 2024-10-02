import random
import matplotlib.pyplot as plt

# n = k + 1 nodes
# p = probability of flipping
# s = number of sequences created

def createSequences(n, p, s):
  sequences = []
  
  for i in range(s):
    sequence = []
    x = random.randint(0,1) # first node
    sequence.append(x)
    for j in range(1, n):     # remaining nodes
      if random.random() < p:
        x = 1 - x
      sequence.append(x)
    sequences.append(sequence)
  return sequences


def printSequence(sequences):
  for sequence in sequences:
    print(sequence)
  return


#def sortSequences(sequences):
#  typeA = [] # same start and end node values
#  typeB = [] # different start and end node values
#  
#  for sequence in sequences:
#    if sequence[0] == sequence[-1]:
#      typeA.append(sequence)
#    else:
#      typeB.append(sequence)
#  return typeA, typeB


def calculatePr(sequence, k):
  # how many sequences where x0 = xk , divided by number of sequences
  count = 0
  for seq in sequence:
    if seq[0] == seq[k]:
      count+=1
  return round((count/len(sequence)), 2)


def plotPr(node_counts, probabilities):
  plt.plot(node_counts, probabilities, marker='o')
  plt.xticks(node_counts)
  plt.xlabel('Number of Nodes')
  plt.ylabel('Probability that x0 = xk')
  plt.title('Probability of x0 = xk vs Number of Nodes')
  plt.ylim(0, 1)
  plt.grid()
  plt.show()


def match(sequences, known):
    matchSequences = []
    for sequence in sequences:
        match == True
        for node in known:
            if sequence[node['index']] != node['value']:
                match == False
                break
        if match:
            matchSequences.append(sequence)
    return matchSequences
    
    
def sortIntervals(sequences, known):
    typeA = []
    typeB = []
    knownIndices = [node['index'] for node in known]
    
    for sequence in sequences:
        if knownIndices[0] > 0: # left interval
            leftInterval = sequence[:knownIndices[0]]
            if leftInterval and leftInterval[0] == leftInterval[-1]:
                typeA.append(leftInterval)
            else:
                typeB.append(rightInterval)
        for i in range(len(known_indices) - 1):
            start = knownIndices[i]
            end = knownIndices[i + 1]
            betweenInterval = sequence[start:end]
            if betweenInterval and betweenInterval[0] == betweenInterval[-1]:
                typeA_intervals.append(betweenInterval)
            else:
                typeB_intervals.append(betweenInterval)
        if knownIndices[-1] < len(sequence): # right interval
            rightInterval = sequence[known_indices[-1] + 1:]
            if rightInterval and rightInterval[0] == rightInterval[-1]:
                typeA.append(rightInterval)
            else:
                typeB.append(rightInterval)
    return typeA, typeB
    

#def estimate(sequence, known):
#    count = 0
#    for node in known:
#    TODO
        
        
def main(): # Not working yet
  p = 0.25  # Probability
  s = 50000 # Sequences generated
  k = 1     # Desired index
  nodes = range(2,21)
  matchSequences = []
  probabilitiesA = []
  probabilitiesB = []
  
  # Nodes with values we know, using dictionary
  knownNodes = [{'index': 1, 'value': 0}, {'index': 2, 'value': 1}, {'index': 3, 'value': 0}, {'index': 4, 'value': 1}]

  for n in nodes:
    sequences = createSequences(n, p, s)
    matchSequences = match(sequences, knownNodes)
    typeA, typeB = sortIntervals(sequences)
    if k < n and k > 0: # check if k is in the range of n nodes
        probabilityA = calculatePr(typeA, k)
        probabilitiesA.append(probabilityA)
        probabilityB = calculatePr(typeB, k)
        probabilitiesB.append(probabilityB)
    else:
        print("Out of bounds")
    #printSequence(typeA)
    #printSequence(probabilitiesA)

  plotPr(nodes, probabilitiesA)


if __name__ == "__main__":
    main()
