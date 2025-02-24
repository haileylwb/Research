import random
import matplotlib.pyplot as plt
import numpy as np

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
# p = probability of flippinga
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
    if count1 > count0:
        majorityValue += 1
    elif count1 == count0:
        majorityValue += random.randint(0, 1)
    else:
        majorityValue += 0 # haha
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
    elif count1 == count0:
        majorityValue += random.randint(0, 1)
    else:
        majorityValue += 0 # haha
    return majorityValue
    

# Checks if sequences match sample

def matchSample(sequences, sample):
    matchedSeq = []
    indexList = [item['index'] for item in sample]
    for sequence in sequences:
        match = True
        for i in range(len(indexList)):
            if sequence[indexList[i]] != sample[i]["value"]:
                match = False
                break
        if match:
            matchedSeq.append(sequence)
    return matchedSeq


# Calculate Pr(Majority = Majority in Sample | Samples)

def majorityWorks(n, p, s, samples):
    sum = []
    
    for sample in samples:
        majS = majorityValueDictionary(sample)
        majorityMatch = 0
        sequences = createSequences(n, p, s)
        
        matches = matchSample(sequences, sample)
        
        for match in matches:
            majG = majorityValueList(match)
            if majS == majG:
                majorityMatch += 1

        if len(matches) == 0:
            prMajority = 0
        else:
            prMajority = majorityMatch / len(matches)

        sum.append(prMajority)
    return sum
    

# Calculate Pr(Majority = Majority in Sample | Locations)

def majorityGivenLocation(n, p, s, locations):
    sequences = createSequences(n, p, s)
    match = 0
    
    for sequence in sequences:
        majG = majorityValueList(sequence)
        
        locationValues = []
        for l in locations:
            locationValues.append(sequence[l])
        majS = majorityValueList(locationValues)
        if (majG == majS):
            match+=1
        
    return match / s

    
# -----------------------------------------------------------------------------------------------

# GRAPHING FUNCTIONS

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


# Graph p vs P(G = S | S)

def plotMajorityWorksVsProbability(probabilities, s, knowns):
    plt.figure(figsize=(10, 6))
    majority_proportions = []

    for p in probabilities:
        result = majorityWorks(11, p, s, knowns)
        majority_proportions.append(result)
        
    plt.plot(probabilities, majority_proportions, marker='o')

    plt.xlabel('Probability (p)')
    plt.ylabel('Pr(Maj G = Maj S)')
    plt.title('P vs Pr(Maj G = Maj S | S)')
    plt.grid(True)
    
    plt.ylim(0, 1)
    plt.yticks([i * 0.1 for i in range(11)])
    
    plt.show()


# Graph p vs P(G = S | S locations)

def plotMajorityWorksGivenLocations(n, probabilities, s, location_sets):
    plt.figure(figsize=(10, 6))

    for locations in location_sets:
        results = []

        for p in probabilities:
            result = majorityGivenLocation(n, p, s, locations)
            results.append(result)

        label = f"Locations: {locations}"
        plt.plot(probabilities, results, label=label)

    plt.xlabel('Probability (p)')
    plt.ylabel('Pr(Maj G = Maj S)')
    plt.title('Probability vs Pr(Maj G = Maj S | S locations)')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.yticks([i * 0.1 for i in range(11)])
    plt.legend()

    plt.show()
    

# Graphs p vs P(G = S | S locations), sorted by sample size

def plotAveragedMajorityBySampleSize(n, probabilities, s, location_sets):
    from collections import defaultdict

    plt.figure(figsize=(10, 6))

    # Group locations by the number of sample points
    grouped_locations = defaultdict(list)
    for loc_set in location_sets:
        grouped_locations[len(loc_set)].append(loc_set)

    # Compute and plot averaged probability for each group
    for sample_size, locations in grouped_locations.items():
        averaged_probabilities = []

        for p in probabilities:
            total_prob = 0
            for loc in locations:
                total_prob += majorityGivenLocation(n, p, s, loc)
            averaged_probabilities.append(total_prob / len(locations))  # Average for group

        plt.plot(probabilities, averaged_probabilities, marker='o', label=f"{sample_size} Sample Points")

    # Plot settings
    plt.xlabel('Probability (p)')
    plt.ylabel('Average Pr(Maj G = Maj S)')
    plt.title('Probability vs Averaged Pr(Maj G = Maj S) by Sample Size')
    plt.grid(True)
    plt.ylim(0, 1)
    plt.yticks([i * 0.1 for i in range(11)])
    plt.legend(title="Number of Sample Points")
    plt.show()


# Print for testing

def printSequence(sequences):
    for sequence in sequences:
        print(sequence)
    return
    

# -----------------------------------------------------------------------------------------------


# Main method

def main():
    # Generate 10^6 sequences
    s = 1000000
    
    # Probabilities
    prob = np.arange(0.01, 0.51, 0.01).tolist()
    
    # Nodes
    nodes = range(11,31,1)
    
    # Known locations -----------------------------------------------------------------
        
    location_sets = [[0, 1, 2], [3, 6, 9], [4, 6, 8], [3, 5, 7], [2, 5, 8]]
    location_spaced_by_one = [[0, 2, 4, 6, 8, 10], [1, 3, 5, 7, 9]]
    location_spaced_by_two = [[0, 3, 6, 9], [1, 4, 7, 10]]
    location_spaced_by_three = [[0, 4, 8], [2, 6, 10]]
    location_spaced_by_four = [[0, 5, 10]]
    location_spaced_odd = [[1, 3, 5, 7, 9], [0, 4, 8], [2, 6, 10], [0, 5, 10]]
    location_all_spacing = [[0, 2, 4, 6, 8, 10], [1, 3, 5, 7, 9], [0, 3, 6, 9], [1, 4, 7, 10], [0, 4, 8], [2, 6, 10], [0, 5, 10]]
    
    location_spaced_by_sample_size = [[0, 4, 8], [2, 6, 10], [0, 5, 10]]
    
#    plotMajorityWorksGivenLocations(11, prob, s, location_all_spacing)
#    plotMajorityWorksGivenLocations(11, prob, s, location_all_spacing)
    plotAveragedMajorityBySampleSize(11, prob, s, location_all_spacing)

#    graphThreeSampleLocations(11, prob, s)
    
    
    # Known location and values ------------------------------------------------------
    
    # Knowns
    # Not very efficient way of coding this ..
    # Sorted by locations
    knowns = [ # Locations: 0 1 2
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 0}, {'index': 2, 'value': 0}],
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 0}, {'index': 2, 'value': 1}],
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 1}, {'index': 2, 'value': 0}],
        [{'index': 0, 'value': 1}, {'index': 1, 'value': 0}, {'index': 2, 'value': 0}]
    ]
    knowns2 = [ # Locations: 3 6 9
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 0}, {'index': 9, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 0}, {'index': 9, 'value': 1}],
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 1}, {'index': 9, 'value': 0}],
        [{'index': 3, 'value': 1}, {'index': 6, 'value': 0}, {'index': 9, 'value': 0}]
    ]
    knowns3 = [ # Locations: 4 6 8
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 0}, {'index': 8, 'value': 0}],
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 0}, {'index': 8, 'value': 1}],
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 1}, {'index': 8, 'value': 0}],
        [{'index': 4, 'value': 1}, {'index': 6, 'value': 0}, {'index': 8, 'value': 0}]
    ]
    knowns4 = [ # Locations: 3 5 7
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 0}, {'index': 7, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 0}, {'index': 7, 'value': 1}],
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 1}, {'index': 7, 'value': 0}],
        [{'index': 3, 'value': 1}, {'index': 5, 'value': 0}, {'index': 7, 'value': 0}]
    ]
    
    # Sorted by values
    knowns5 = [ # Values: 0 0 0
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 0}, {'index': 2, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 0}, {'index': 9, 'value': 0}],
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 0}, {'index': 8, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 0}, {'index': 7, 'value': 0}],
        [{'index': 2, 'value': 0}, {'index': 5, 'value': 0}, {'index': 8, 'value': 0}]
    ]
    knowns6 = [ # Values: 0 0 1
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 0}, {'index': 2, 'value': 1}],
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 0}, {'index': 9, 'value': 1}],
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 0}, {'index': 8, 'value': 1}],
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 0}, {'index': 7, 'value': 1}],
        [{'index': 2, 'value': 0}, {'index': 5, 'value': 0}, {'index': 8, 'value': 1}]
    ]
    knowns7 = [ # Values: 0 1 0
        [{'index': 0, 'value': 0}, {'index': 1, 'value': 1}, {'index': 2, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 6, 'value': 1}, {'index': 9, 'value': 0}],
        [{'index': 4, 'value': 0}, {'index': 6, 'value': 1}, {'index': 8, 'value': 0}],
        [{'index': 3, 'value': 0}, {'index': 5, 'value': 1}, {'index': 7, 'value': 0}],
        [{'index': 2, 'value': 0}, {'index': 5, 'value': 1}, {'index': 8, 'value': 0}]
    ]
    knowns8 = [ # Values: 1 0 0
        [{'index': 0, 'value': 1}, {'index': 1, 'value': 0}, {'index': 2, 'value': 0}],
        [{'index': 3, 'value': 1}, {'index': 6, 'value': 0}, {'index': 9, 'value': 0}],
        [{'index': 4, 'value': 1}, {'index': 6, 'value': 0}, {'index': 8, 'value': 0}],
        [{'index': 3, 'value': 1}, {'index': 5, 'value': 0}, {'index': 7, 'value': 0}],
        [{'index': 2, 'value': 1}, {'index': 5, 'value': 0}, {'index': 8, 'value': 0}]
    ]


# Run main method

if __name__ == "__main__":
    main()

