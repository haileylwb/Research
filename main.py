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
    knowns = {node['index']: node['value'] for node in known}
    
    for i in range(s):
        sequence = [None] * n
        # Set knowns
        for index, value in knowns.items():
            sequence[index] = value
        knownIndexList = list(knowns.keys())
        firstKnownIndex = knownIndexList[0]
        lastKnownIndex = knownIndexList[-1]

        # Before first known
        for j in range(firstKnownIndex, -1, -1):
            if sequence[j] is None:
                x = sequence[j + 1]
                if random.random() < p:
                    sequence[j] = 1 - x
                else:
                    sequence[j] = x
        # After last known
        for k in range(lastKnownIndex, n):
            if sequence[k] is None:
                x = sequence[k - 1]
                if random.random() < p:
                    sequence[k] = 1 - x
                else:
                    sequence[k] = x

        # Rejection sampling in the middle
        for m in range(len(knownIndexList) - 1):
            startIndex = knownIndexList[m]
            endIndex = knownIndexList[m + 1]

            matched = False
            while not matched:
                temp_sequence = createSequences(endIndex - startIndex + 1, p, 1)[0]
                if (temp_sequence[0] == sequence[startIndex]) and (temp_sequence[-1] == sequence[endIndex]):
                    for index in range(startIndex + 1, endIndex):
                        sequence[index] = temp_sequence[index - startIndex]
                    matched = True

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


# Creates random known values for a fixed number of knowns n//3
# Has more 1's than 0's
def randomSampling(n):
    knownNodes = []
    if n < 3:
        knownNodes.append({'index': 0, 'value': 1})
    else:
        numKnown = n // 3
        # The number of 1's will be half or half+1 the number of knowns
        # The number of 1's will be at least half to up to all the knowns
        majorityCount = (numKnown // 2) + 1
        #majorityCount = random.randint((numKnown // 2) + 1, numKnown)
        minorityCount = numKnown - majorityCount
        knownIndices = random.sample(range(n), numKnown)

        for index in knownIndices:
            if majorityCount > 0:
                knownNodes.append({'index': index, 'value': 1})
                majorityCount -= 1
            else:
                knownNodes.append({'index': index, 'value': 0})
    knownNodes.sort(key=lambda x: x['index'])
    return knownNodes


# Calculate the proportion of the majority value in the sequences
def majorityProportion(sequences):
    n = len(sequences)
    m = len(sequences[0])
    majorityCount = 0
    
    for sequence in sequences:
        count1 = sum(sequence)
        count0 = m - count1
        
        if count1 > count0:
            majorityCount += 1
            
    return majorityCount / n
    
# k = given index
# Calculates how many sequences satisfy x0 = xk, divided by number of sequences

def calculatePr(sequence, k):
    count = 0
    for seq in sequence:
        if seq[0] == seq[k]:
            count += 1
    return round((count/len(sequence)), 2)
    

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
    
    
# Calculates proportion of sequences that have more 0's than 1's

def more1(sequences):
    n = len(sequences)
    more1sequences = 0
    
    for sequence in sequences:
        count = 0
        m = len(sequence)
        count += sum(sequence)
        if count > (m - count):
            more1sequences += 1
    return more1sequences / n
    

# Calculates proportion of sequences that have equal number of 0's and 1's

def equal01(sequences):
    n = len(sequences)
    equalSequences = 0
    
    for sequence in sequences:
        count = 0
        m = len(sequence)
        count += sum(sequence)
        if count == (m - count):
            equalSequences += 1
    return equalSequences / n
    
    
# Calculate Pr( X(k) = V | X(0) = V, X(k+2) = V)
# When k = 1, we get ((1-p) * (1 + (1-2p)^k)) / (1 + (1-2p)^k)


# We have node X(i) and X(i+k+1) with the SAME value V, with k nodes in-between
# For each node, calculate the probability it has value V
# Use the math summation thingy we found
# The sum of the probabilities will be the estimated number of V's in-between
# Expected # of not V = k - Expected # of V

def estimateInBetweenSame(k, v, p):
    expected = 0
    # By symmetry, we can just calculate the first half and multiply by 2
    end = (k // 2)
    for i in range(end):
        expected += 1 #CHANGE THIS
        
    # If there is an odd number of nodes, calculate middle node separately
    if (k % 2) == 1:
        mid = k // 2
        expected += 1 # CHANGE THIS
    return expected
    

# We have node X(i) and X(i+k+1) with the DIFFERENT VALUES, with k nodes in-between
# For each node, calculate the probability it has value V
# Use the math summation thingy we found
# The sum of the probabilities will be the estimated number of V's in-between

#def estimateInBetweenSame(k, v):
#    return
    
    

# Graphs the average % majority on the y-axis with n nodes on the x-axis
def plotAverageMajority(node_counts, probabilities):
    plt.plot(node_counts, probabilities, marker='o')
    plt.xticks(node_counts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average % Majority')
    plt.title('Average Majority Proportion vs Number of Nodes')
    plt.ylim(0, 1)
    plt.grid()
    plt.show()


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


# Print for testing

def printSequence(sequences):
    for sequence in sequences:
        print(sequence)
    return
    

# -----------------------------------------------------------------------------------------------


# Main method

def main():
    p = 0.2         # Probability
    s = 50000      # Sequences generated
    #k = 1          # Desired index
    nodes = range(5,30)
    #nodes = [31, 33, 35, 37, 39, 41, 43, 45, 75, 77, 79, 81, 83, 85]
    proportions = []
    
    # Nodes with values we know, using dictionary
#    knownNodes = [{'index': 0, 'value': 1}, {'index': 1, 'value': 1}, {'index': 2, 'value': 0}, {'index': 5, 'value': 0}, {'index': 6, 'value': 1}]
    
    for n in nodes:
        sequences = []
#        knownNodes = [{'index': 0, 'value': 1}, {'index': 1, 'value': 1}, {'index': 2, 'value': 1}, {'index': n-2, 'value': 0}, {'index': n-1, 'value': 0}]

        # For every sample generated, we want there to be a new dictionary of knownNodes
        for i in range(s):
            knownNodes = randomSampling(n)
            sequence = createSequencesKnown(n, p, 1, knownNodes)
            sequences.append(sequence[0])

        proportion = majorityProportion(sequences)
        proportions.append(proportion)
            
#        print(f"Sequences with {n} nodes:")
#        print("Average number of 0's: " + str(avg0(sequences)))
#        print("Proportion of Sequences with More 0's: " + str(more0(sequences)))
#        print("Proportion of Sequences with More 1's: " + str(more1(sequences)))
#        print("Proportion of Sequences with Equal 0's and 1's: " + str(equal01(sequences)))
#        print("---")

    plotAverageMajority(nodes, proportions)

# Run main method

if __name__ == "__main__":
    main()
