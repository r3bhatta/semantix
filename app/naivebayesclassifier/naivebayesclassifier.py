from nltk.probability import ELEProbDist, FreqDist
from nltk import NaiveBayesClassifier
from collections import defaultdict
import os
import settings

testingSet = {
    'We are at 444 Weber Street',
    'steak bread hot dog',
    '888 Socks Drive',
    'chicken broccoli lol',
    '8 oz steak',
    'turkey club',
    '2:00 pm'
}

def labels():
    return ['menu', 'location', 'noise','hours']

def trainingSet():
    def createTrainingDict(fileName, category):
        trainingSet = {}
        with open(fileName) as file:
            lines = file.readlines()
            for line in lines:
                trainingSet[line.strip()] = category
        return trainingSet

    def training(files, label):
        for file in files:
            trainingSet.update(createTrainingDict(os.path.join(settings.APP_DATA_ASSETS, file), label))

    trainingSet = {}
    locationFiles = ['countries', 'states', 'addresses']
    menuFiles = ['menus']
    hoursFiles = ['hours']
    noiseFiles = ['noise']


    training(locationFiles, 'location')
    training(menuFiles, 'menu')
    training(hoursFiles, 'hours')
    training(noiseFiles, "noise")

    return trainingSet

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def splitTrue(item):
    words = item.split()
    splits = {}
    for word in words:
        # Consider all numbers as one category.
        if isInt(word):
            word = 'number'
        splits[word.lower()] = True
    return splits

# Generates features set: {'steak': {'menu': 1, 'location': 0}}.
def generateFeaturesSet(trainingSet):
    def generateDefaultFreq():
        frequencies = {}
        for category in labels():
            frequencies[category] = 0
        return frequencies

    frequencies = {}
    for text, label in trainingSet.items():
        tokens = text.split()
        for token in tokens:
            # Consider all numbers as one category.
            if isInt(token):
                token = 'number'
            if token not in frequencies:
                frequencies[token] = generateDefaultFreq()
            frequencies[token][label] += 1
    return frequencies

# Generates expected likelihood distribution for labels.
def getLabelProbabilityDistribution(features):
    labelFrequencies = FreqDist()
    for item, counts in features.items():
        for label in labels():
            if counts[label] > 0:
                labelFrequencies.inc(label)
    return ELEProbDist(labelFrequencies)

# Generates expected likelihood distribution for features.
def getFeatureProbabilityDistribution(features):
    frequencyDistributions = defaultdict(FreqDist)
    values = defaultdict(set)
    numberSamples = len(trainingSet()) / 2
    for token, counts in features.items():
        for label in labels():
            frequencyDistributions[label, token].inc(True, count = counts[label])
            frequencyDistributions[label, token].inc(None, numberSamples - counts[label])
            values[token].add(None)
            values[token].add(True)
    '''
    for item in frequencyDistributions.items():
        print item[0], item[1]
    '''
    probabilityDistribution = {}
    for ((label, name), freqDist) in frequencyDistributions.items():
        eleProbDist = ELEProbDist(freqDist, bins = len(values[name]))
        probabilityDistribution[label, name] = eleProbDist
    return probabilityDistribution

featuresSet = generateFeaturesSet(trainingSet())

labelProbabilityDistribution = getLabelProbabilityDistribution(featuresSet)

featureProbabilityDistribution = getFeatureProbabilityDistribution(featuresSet)

classifier = NaiveBayesClassifier(labelProbabilityDistribution, featureProbabilityDistribution)

def classify(item):
    label = classifier.classify(splitTrue(item.lower()))
    return (label, classifier.prob_classify(splitTrue(item.lower())).prob(label))


for item in testingSet:
    result = classify(item)
    print "%s | %s | %s" % (item, result[0], result[1])


#classifier.show_most_informative_features()
