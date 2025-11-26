def to_list_of_lists(frequencies, response_items):
    collectionFreqs = []
    Cindex = 0  # index for the collectionFreqs
    RIindex = 0 # tracks index on how many response items 
  
    for f in frequencies:
        if Cindex >= len(collectionFreqs):
            collectionFreqs.append([])  # Append a new list to collectionFreqs if needed
      
        collectionFreqs[Cindex].append(f) # Append f to the appropriate list in collectionFreqs
    
        if len(collectionFreqs[Cindex]) >= len(response_items):
            # one list in collectionFreqs has been completed, thus jumps onto next list
            Cindex += 1 # next list
            RIindex = 0
        else:
            RIindex += 1 # next response item and frequency

    return collectionFreqs

def getMean(q_and_frequencies, q_and_tweights):
        mean = {}

        # loop through the list to get the weightedValues and add it to totalWeight immediately
        for q in q_and_frequencies:
            mean[q] = round(q_and_tweights[q] / sum(q_and_frequencies[q]), 2)

        return mean

def getFMsquared(self):  # (FM) times Midpoint
    FMsquared = []
    weightedValues = self.getWeightedValues()
    for i, f in enumerate(weightedValues):
        FMsquared.append((i + 1) * weightedValues[i])

    return FMsquared

def getVariance(self):
    variance = 0

    # provide the values in the table or as needed
    mean = self.getMean()
    FMsquared = self.getFMsquared()

    summationFMsquared = 0
    for value in FMsquared:
        summationFMsquared += value

    # Formula for Variance:
    variance = (summationFMsquared / (self.totalFrequency - 1)) - ((self.totalFrequency * (mean ** 2)) / (self.totalFrequency - 1))

    return round(variance, 2)    

def getMedian(q_and_frequencies):
    medians = {}

    for q in q_and_frequencies:
        observation = (sum(q_and_frequencies[q]) + 1)/2
        for i in q_and_frequencies[q]:
            if i >= observation:
                medians[q] = q_and_frequencies[q].index(i) +1
   
    return medians

def getMode(self):
    mode = []
    highestFrequency = max(self.frequency)  # get highest frequency

    # find category* that have the highest frequency and store it in a list
    for i, f in enumerate(self.frequency):
        if f == highestFrequency:
            mode.append(i + 1)
    return mode