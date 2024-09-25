import random

# n = k + 1 nodes
# p = probability of flipping
# s = number of sequences created
def createSequences(n, p, s):
  sequences = []

  for i in range(s):
    sequence = []

    # X0 first node
    x = random.randint(0,1)
    sequence.append(x)

    # Rest of the nodes
    for j in range(1, n):
      if random.randint(0,100) < p*100
        x = 1 - x
      sequence.append(x)

    sequences.append(sequence)
    
  return sequences

def printSequence(n, p, s):
  sequences = createSequences(n, p, s)
  for sequence in sequences:
    print(sequence)
