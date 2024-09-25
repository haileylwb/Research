import random
import matplotlib.pyplot as plt

# n = k + 1 nodes
# p = probability of flipping
# s = number of sequences created
def createSequences(n, p, s):
  sequences = []
  
  for i in range(s):
    sequence = []
    
    # first node
    x = random.randint(0,1)
    sequence.append(x)
    
    # remaining nodes
    for j in range(1, n):
      if random.random() < p:
        x = 1 - x
      sequence.append(x)
      
    sequences.append(sequence)
  return sequences


def printSequence(sequences):
  for sequence in sequences:
    print(sequence)
  return


def sortSequences(sequences):
  typeA = [] # same start and end node values
  typeB = [] # different start and end node values

  for sequence in sequences:
    if sequence[0] == sequence[-1]:
      typeA.append(sequence)
    else:
      typeB.append(sequence)

  return typeA, typeB


def calculatePr(sequence):
  # how many sequences where x1 = x0 , divided by number of sequences
  count = 0
  for seq in sequence:
    if seq[0] == seq[1]:
      count+=1
  return round(count/len(sequence))


def plotPr(node_counts, probabilities):
  plt.plot(node_counts, probabilities, marker='o')
  plt.xticks(node_counts)
  plt.xlabel('Number of Nodes')
  plt.ylabel('Probability that x1 = x0')
  plt.title('Probability of x1 = x0 vs Number of Nodes')
  plt.ylim(0, 1) 
  plt.grid()
  plt.show()

  
def main():
  p = 0.5  
  s = 100
  nodes = range(2, 11)  # Node from 2 to 10
  probabilitiesA = []
  probabilitiesB = []

  for n in nodes:
    sequences = createSequences(n, p, s)
    typeA, typeB = sortSequences(sequences)
    probabilityA = calculatePr(typeA)
    probabilitiesA.append(probabilityA)
    probabilityB = calculatePr(typeB)
    probabilitiesA.append(probabilityB)

  plotPr(node_counts, probabilitiesA)


if __name__ == "__main__":
    main()
  
