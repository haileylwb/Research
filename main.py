import random
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------------------------

# GENERATING FUNCTIONS

# -----------------------------------------------------------------------------------------------

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


# Creates random known values for a fixed number of knowns (n//3)
# Has more 1's than 0's (difference of 1)
def randomSampling(n):
    knownNodes = []
    if n < 3:
        knownNodes.append({'index': 0, 'value': 1})
    else:
        numKnown = n // 3
        if numKnown % 2 == 0:
            majorityCount = numKnown // 2
            minorityCount = majorityCount - 1
            numKnown = majorityCount + minorityCount
        else:
            majorityCount = numKnown // 2 + 1
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


# -----------------------------------------------------------------------------------------------

# COUNTING FUNCTIONS

# -----------------------------------------------------------------------------------------------


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
    
    
# Calculates proportion of sequences that have more 1's than 0's

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
    
    
# -----------------------------------------------------------------------------------------------

# CALCULATING PROBABILITY & ESTIMATING FUNCTIONS

# -----------------------------------------------------------------------------------------------

    
# Calculate Pr( X(x+1) = V | X(0) = V, X(k+1) = V)
# 0.5 + ((1-2p)^i + (1-2p)^(k+1-i)) / (2 * (1 + (1-2p)^(k+1)))

def calculateProbInBetweenSame(k, x, p):
    return 0.5 + ((1-2*p)**x + (1-2*p)**(k+1-x)) / (2 * (1 + (1-2*p)**(k+1)))
    
    
# Expected number of V in between X(i) = X(i+k+1) = V, k nodes in-between

def estimateInBetweenSame(k, p):
    expected = 0
    for i in range(1, k+1):
        expected += calculateProbInBetweenSame(k,i,p)
    return expected
    
    
# Calculate Pr( X(x+1) = V | X(0) = V)
# 0.5 + ((1-2p)^i)/2

def calculateProbRightSame(k, x, p):
    return 0.5 + ((1-2*p)**x)/2
    
    
# Expected number of V's, k nodes after X(i)

def estimateRightSame(k, p):
    expected = 0
    for i in range(1, k+1):
        expected += calculateProbRightSame(k,i,p)
    return expected
    

# Calculate Pr( X(x+1) = V | X(0) = V, X(k+1) = !V)
# 0.5 + ((1-2p)^i - (1-2p)^(k+1-i)) / (2 * (1 - (1-2p)^(k+1)))

def calculateProbInBetweenDiff(k, x, p):
    return 0.5 + ((1-2*p)**x - (1-2*p)**(k+1-x))/ (2 * (1 - (1 - 2*p)**(k+1)))
    

# Expected number of V's in k nodes between X(0) = V and X(k+1) = !V

def estimateInBetweenDiff(k,p):
    expected = 0
    for i in range(1, k+1):
        expected += calculateProbInBetweenDiff(k,i,p)
    return expected
    

# Estimate the number of V's given a sample
# p = probability
# k = number of nodes total
# sample = given sample

def estimate(p, k, knowns):
    exp_0 = 0
    exp_1 = 0
    
    knownsDict = {node['index']: node['value'] for node in knowns}
    
    knownIndexList = sorted(knownsDict.keys())
    
    exp_0 += sum(1 for value in knownsDict.values() if value == 0)

    if knownIndexList:
        firstKnownIndex = knownIndexList[0]
        if knownsDict[firstKnownIndex] == 0:
            exp_0 += estimateRightSame(firstKnownIndex, p)
        else:
            exp_0 += firstKnownIndex - estimateRightSame(firstKnownIndex, p)

        lastKnownIndex = knownIndexList[-1]
        if lastKnownIndex < k - 1:
            numNodesAfterLastKnown = k - lastKnownIndex - 1
            if knownsDict[lastKnownIndex] == 0:
                exp_0 += estimateRightSame(numNodesAfterLastKnown, p)
            else:
                exp_0 += (numNodesAfterLastKnown - estimateRightSame(numNodesAfterLastKnown, p))
    
    # In Betweens
    for m in range(len(knownIndexList) - 1):
        startIndex = knownIndexList[m]
        endIndex = knownIndexList[m + 1]
        nodesInBetween = endIndex - startIndex - 1

        startValue = knownsDict[startIndex]
        endValue = knownsDict[endIndex]
        
        if startValue == 0 and endValue == 0: # 0 ... 0
            exp_0 += estimateInBetweenSame(nodesInBetween, p)
        elif startValue == 1 and endValue == 1: # 1 ... 1
            exp_0 += nodesInBetween - estimateInBetweenSame(nodesInBetween, p)
        else: # 0 ... 1 or 1 ... 0
            exp_0 += estimateInBetweenDiff(nodesInBetween, p)

    exp_1 = k - exp_0
    
    return exp_0, exp_1


# Calculates majority value in a sequence
# Dictionary implementation

def majorityValueDictionary(known):
    count0 = 0
    count1 = 0
    majorityValue = 0
    knowns = {node['index']: node['value'] for node in known}
    valuesList = list(knowns.values())
    for i in valuesList:
        if i == 0:
            count0 += 1
        else:
            count1 += 1
    if count1 > count0:
        majorityValue += 1
    return majorityValue
    
    
# List implementation

def majorityValueList(known):
    count0 = 0
    count1 = 0
    majorityValue = 0
    for i in known:
        if i == 0:
            count0 += 1
        else:
            count1 += 1
    if count1 > count0:
        majorityValue += 1
    return majorityValue
    

# Checks if sequences match sample

def matchSample(sequences, sample):
    matchedSeq = []
    indexList = list(sample[0].keys())
    for sequence in sequences:
        match = True
        for i in indexList:
            if sample[0][i] != sequence.get(i, None):
                match = False
                break
        if match:
            matchedSeq.append[sequence]
    return matchedSeq


# Calculate Pr(Majority = Majority in Sample)

def majorityWorks(n, p, s, samples):
    sum = 0
    for sample in samples:
        sequences = createSequences(n, p, s)
        matches = matchSample(sequences, sample)

#    Calculate majority value on s
#    Calulate majority value on G

#    prMajority =
        prSample = len(matches) / 1000000
        sum += prMajority * prSample
    return sum
        
    
# -----------------------------------------------------------------------------------------------

# GRAPH PLOTTING FUNCTIONS

# -----------------------------------------------------------------------------------------------

    
# Line Graph: Number of Nodes vs Average % Majority

def plotAverageMajority(node_counts, probabilities):
    plt.plot(node_counts, probabilities, marker='o')
    plt.xticks(node_counts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average % Majority')
    plt.title('Average Majority Proportion vs Number of Nodes')
    plt.ylim(0, 1)
    plt.grid()
    plt.show()


# Line Graph: Number of Nodes vs % Majority of 1's and 0's

def plotMajority(node_counts, probabilities0, probabilities1):
    plt.plot(node_counts, probabilities0, marker='o', label='Probabilities 0')
    plt.plot(node_counts, probabilities1, marker='o', label='Probabilities 1', linestyle='--')
    plt.xticks(node_counts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Average % Majority')
    plt.title('Average Majority Proportion vs Number of Nodes')
    plt.ylim(0, 1)
    plt.grid()
    plt.show()


# Line Graph: Number of Nodes vs Probability (x0 = xk)

def plotPr(node_counts, probabilities):
    plt.plot(node_counts, probabilities, marker='o')
    plt.xticks(node_counts)
    plt.xlabel('Number of Nodes')
    plt.ylabel('Probability that x0 = xk')
    plt.title('Probability of x0 = xk vs Number of Nodes')
    plt.ylim(0, 1)
    plt.grid()
    plt.show()


# Bar Graph: Number of Nodes vs Proportion of Majority of 1, 0, Equal

def plotMajorityStackedBar(node_counts, proportions0, proportions1, proportionsE):
    width = 0.6
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.bar(node_counts, proportions1, width, label='Majority 1', color='tab:blue')
    ax.bar(node_counts, proportions0, width, bottom=proportions1, label='Majority 0', color='tab:orange')
    ax.bar(node_counts, proportionsE, width, bottom=[i+j for i,j in zip(proportions1, proportions0)], label='Equal 0 & 1', color='tab:green')

    ax.set_xlabel('Number of Nodes')
    ax.set_ylabel('Proportion of Sequences')
    ax.set_title('Majority Proportions for Sequences with Varying Nodes')
    ax.set_xticks(node_counts)
    ax.set_xticklabels(node_counts)
    ax.legend()

    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


# Print for testing

def printSequence(sequences):
    for sequence in sequences:
        print(sequence)
    return
    

# -----------------------------------------------------------------------------------------------


# Main method

def main():
    # Generate 1 million sequences
    s = 1000000
    
    # Probabilities
    prob = [0.01, 0.05, 0.1, 0.25, 0.5]
    
    # Nodes
    nodes = range(11,31,1)
    
    # Proportions List
    proportions0 = []
    proportions1 = []
    proportionsE = []
    
    # Knowns
    knowns = [
    [{'index': 1, 'value': 0}, {'index': 2, 'value': 0}, {'index': 3, 'value': 0}],
    [{'index': 3, 'value': 0}, {'index': 5, 'value': 0}, {'index': 7, 'value': 0}]
    ]
    
    exmple = [{'index': 0, 'value': 0}, {'index': 1, 'value': 0}, {'index': 2, 'value': 0}]
    
    # Estimation
    print(estimate(.2, 9, exmple))
    
    # Sample and majority works
#    for p in prob:
#        print(p)
#        for known in knowns:
#            createSequences(9, p, s)
    
#    nodes = [30, 31, 32, 33, 34, 35, 36, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
    
#    for n in nodes:
#        sequences = []
#
#        for i in range(s):
#            knownNodes = randomSampling(n)
#            sequence = createSequencesKnown(n, p, 1, knownNodes)
#            sequences.append(sequence[0])
#
#        proportion0 = more0(sequences)
#        proportions0.append(proportion0)
#        proportion1 = more1(sequences)
#        proportions1.append(proportion1)
#        proportionE = equal01(sequences)
#        proportionsE.append(proportionE)
            
#        print(f"Sequences with {n} nodes:")
#        print("Average number of 0's: " + str(avg0(sequences)))
#        print("Proportion of Sequences with More 0's: " + str(more0(sequences)))
#        print("Proportion of Sequences with More 1's: " + str(more1(sequences)))
#        print("Proportion of Sequences with Equal 0's and 1's: " + str(equal01(sequences)))
#        print("---")

#    plotMajority(nodes, proportions0, proportions1)
#    plotMajorityStackedBar(nodes, proportions0, proportions1, proportionsE)
#    print(calculateProbInBetweenSame(1, 1, p))
    
    
# Run main method

if __name__ == "__main__":
    main()
