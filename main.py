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


#def estimate():
# given two node indexes
# take the left side of i (check if i isnt the leftmost node
# take the right side of j (check if j isnt the rightmost node)
# look at the inbetween

# take the number of nodes time the probability of ??
# n - the estimate for the est. number of 1's
 
# if given a list with the index and values
# iterate through the list (assume its sorted increasing order based on index)
# calculate up to the first entry
#
# calculate whatever after the last entry

# _ x _  _ y _ z _ _ _


# def prMoreZeros():
# for all the simulations count how many have more 0's
    
  
def main():
  p = 0.25
  s = 50000
  k = 1 # desired index of node we want to look at
  nodes = range(2,21)  # Nodes from 7 to 20
  probabilitiesA = []
  probabilitiesB = []

  for n in nodes:
    sequences = createSequences(n, p, s)
    typeA, typeB = sortSequences(sequences)
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
