import random
import matplotlib.pyplot as plot

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


def main():
  n = 3
  p = .5
  s = 3
  
  sequences = createSequences(n, p, s)
  typeA, typeB = sortSequences(sequences)
  printSequence(typeA)
  printSequence(typeB)

if __name__ == "__main__":
    main()
  
