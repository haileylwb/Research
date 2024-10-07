import random
import matplotlib.pyplot as plt


# n = k + 1 nodes
# p = probability of flipping
# s = number of sequences created

def createSequences(n, p, s):
    sequences = []
  
    for i in range(s):
        sequence = []
        x = random.randint(0,1)     # First node
        sequence.append(x)
        for j in range(1, n):       # Remaining nodes
            if random.random() < p:
                x = 1 - x
            sequence.append(x)
        sequences.append(sequence)
    return sequences


# n = number of nodes
# p = probability of flipping
# s = number of sequences
# Create sequences given known values and indices

def createSequencesKnown(n, p, s, known):
    sequences = []
    knownIndices = {node['index']: node['value'] for node in known}
    
    for i in range(s):
        sequence = [None] * n
        for index, value in knownIndices.items():  # Set knowns
            sequence[index] = value
        if 0 not in knownIndices:
            x = random.randint(0,1)                # First node
            sequence[0] = x
        for j in range(1, n):                      # Other nodes
            if sequence[j] is None:
                x = sequence[j - 1]
                if random.random() < p:
                    sequence[j] = 1 - x
                else:
                    sequence[j] = x
        sequences.append(sequence)
    return sequences


# Sorts sequences by same or different starting and ending nodes

#def sortSequences(sequences):
#   typeA = [] # same start and end node values
#   typeB = [] # different start and end node values
#
#   for sequence in sequences:
#       if sequence[0] == sequence[-1]:
#           typeA.append(sequence)
#   else:
#       typeB.append(sequence)
#   return typeA, typeB


# k = given index
# Calculates how many sequences satisfy x0 = xk, divided by number of sequences

def calculatePr(sequence, k):
    count = 0
    for seq in sequence:
        if seq[0] == seq[k]:
            count += 1
    return round((count/len(sequence)), 2)


# Graphing the probability that x0 = xk for varying number of nodes

def plotPr(node_counts, probabilities):
    plt.plot(node_counts, probabilities, marker='o')
    plt.xticks(node_counts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Probability that x0 = xk')
    plt.title('Probability of x0 = xk vs Number of Nodes')
    plt.ylim(0, 1)
    plt.grid()
    plt.show()


# Calculates average number of 0's

def avg0(sequences):
    n = len(sequences)
    m = len(sequences[0])
    count = 0
    for sequence in sequences:
        count += sum(sequence) # counts number of 1's in each sequence
    return (n * m - count) / n # average number of 0's


# Calculates proportion of sequences that have more 0's than 1's

def more0(sequences):
    n = len(sequences)
    more0sequences = 0
    
    for sequence in sequences:
        count = 0
        m = len(sequence)
        count += sum(sequence)
        if count < (m - count):
            more0sequences += 1
    return more0sequences / n


# Print for testing

def printSequence(sequences):
    for sequence in sequences:
        print(sequence)
    return


# ------------------------------------------------------------------------------


# Main method

def main():
    p = 0.25        # Probability
    s = 500000      # Sequences generated
    #k = 1          # Desired index
    nodes = range(10,11)
    sequences = []
    
    # Nodes with values we know, using dictionary
    knownNodes = [{'index': 1, 'value': 0}, {'index': 4, 'value': 1}, {'index': 6, 'value': 0}]
    
    for n in nodes:
        sequences = createSequencesKnown(n, p, s, knownNodes)
        #printSequence(sequences)
    print("Average number of 0's")
    print(avg0(sequences))
    print("Proportion of Sequences with More 0's")
    print(more0(sequences))


# Run main method

if __name__ == "__main__":
    main()
