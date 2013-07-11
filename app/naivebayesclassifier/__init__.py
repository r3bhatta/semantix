from nltk.probability import ELEProbDist, FreqDist
import nltk
from collections import defaultdict
import os
from os import listdir
from os.path import isfile, join
import settings

"""
Example:
nbc = NaiveBayesClassifier()
item = nbc.classify("classify this")
# By default this will train data like menus, locations, hours.
# If you want to train other preset data, do this:
nbc.train("businesses")
# This will reset the classifier with the "businesses" data.

Supported train() parameters:
"businesses", "data"
"""
class NaiveBayesClassifier:   
    """
    These private variables are initialized by self.train()
        self.labels - ['label1, label2']
        self.__trainingSet - {'feature': ['label1, label2']}
        self.__featuresSet - {'feature: {'label1': 1, 'label2': 0}}
        self.__labelProbabilityDistribution
        self.__featureProbabilityDistribution
    """
    def __init__(self):
        # Start training.
        self.train()

    """ Creates and returns a training set (dictionary) from one data file belonging to a label. """
    def __updateTrainingSet(self, fileName, label):
        trainingSet = defaultdict(list)
        with open(fileName) as trainingFile:
            lines = trainingFile.readlines()
            for line in lines:
                trainingSet[line.strip()].append(label)
        # Add the new features:labels to the training set.
        for item, labels in trainingSet.items():
            self.__trainingSet[item].extend(labels)

    """
    Train the classifier by iterating through the folder that contains the data.
    @param trainingDataType = 'data' or 'businesses' so far.
    """
    def __generateTrainingSet(self, trainingDataType='data'):
        # Use a defaultdict(list) because the same feature can belong to multiple labels.
        self.__trainingSet = defaultdict(list)
        self.labels = []
        # Ignore some OS generated files, as well as default folders that should not be included.
        # For example, we ignore 'businesses', but if we need 'businesses' we will only be looking
        # inside 'businesses' folder and nothing else.
        # Could be changed!
        ignores = ['.DS_Store', 'businesses']

        trainingDirectory = settings.APP_DATA_TRAINING
        # Change directory to appropriate training data.
        if trainingDataType == 'businesses':
            trainingDirectory = os.path.join(trainingDirectory, trainingDataType)

        # Loop through each folder name for the training folder. The folder name corresponds to a label.
        for label in listdir(trainingDirectory):
            if label not in ignores:
                # Add the folder name as a 'label'.
                self.labels.append(label)
                # Obtain the absolute path of the folder.
                path = os.path.join(trainingDirectory, label)
                # Loop through each training file of each folder.
                for fileName in [f for f in listdir(path) if isfile(join(path, f))]:
                    # Obtain the absolute path of the file.
                    absFileName = os.path.join(path, fileName)
                    # Update the training set dictionary with the training set from the file.
                    self.__updateTrainingSet(absFileName, label)

    """ Check if a string is an integer. """
    def __isInt(self, s):
        try: 
            int(s)
            return True
        except ValueError:
            return False

    """ Split the item being classified into true kvps for dictionary. """
    def __splitTrue(self, item):
        words = item.split()
        splits = {}
        for word in words:
            # Consider all numbers as one category.
            if self.__isInt(word):
                word = 'number'
            splits[word.lower()] = True
        return splits

    """ Generates the features set. """
    def __generateFeaturesSet(self):
        def generateDefaultFreq():
            frequencies = {}
            for label in self.labels:
                frequencies[label] = 0
            return frequencies

        featuresSet = {}
        for text, labels in self.__trainingSet.items():
            tokens = text.split()
            for token in tokens:
                # Consider all numbers as one category.
                if self.__isInt(token):
                    token = 'number'
                if token not in featuresSet:
                    featuresSet[token] = generateDefaultFreq()
                # Loop through all labels associated with this feature.
                for label in labels:
                    featuresSet[token][label] += 1
        self.__featuresSet = featuresSet

    """ Generates expected likelihood distribution for labels. """
    def __generateLabelProbabilityDistribution(self):
        # Print this out to look at how many items were trained for each label.
        labelFrequencies = FreqDist()
        for item, counts in self.__featuresSet.items():
            for label in self.labels:
                if counts[label] > 0:
                    labelFrequencies.inc(label)

        self.__labelProbabilityDistribution = ELEProbDist(labelFrequencies)

    """ Generates expected likelihood distribution for features. """
    def __generateFeatureProbabilityDistribution(self):
        frequencyDistributions = defaultdict(FreqDist)
        values = defaultdict(set)
        numberSamples = len(self.__trainingSet) / 2
        for token, counts in self.__featuresSet.items():
            for label in self.labels:
                frequencyDistributions[label, token].inc(True, count = counts[label])
                frequencyDistributions[label, token].inc(None, numberSamples - counts[label])
                values[token].add(None)
                values[token].add(True)
        probabilityDistribution = {}
        for ((label, name), freqDist) in frequencyDistributions.items():
            eleProbDist = ELEProbDist(freqDist, bins = len(values[name]))
            probabilityDistribution[label, name] = eleProbDist

        self.__featureProbabilityDistribution = probabilityDistribution

    """
    Train the classifier.
    @param trainingDataType = 'data' or 'businesses' so far.
    """
    def train(self, trainingDataType='data'):
        self.__generateTrainingSet()
        self.__generateFeaturesSet()
        self.__generateLabelProbabilityDistribution()
        self.__generateFeatureProbabilityDistribution()
        self.__classifier = nltk.NaiveBayesClassifier(self.__labelProbabilityDistribution, self.__featureProbabilityDistribution)

    """ Classify an item. """
    def classify(self, item):
        label = self.__classifier.classify(self.__splitTrue(item.lower()))
        return (label, self.__classifier.prob_classify(self.__splitTrue(item.lower())).prob(label))

    """ Print some demo items. """
    def demo(self):
        testingSet = {
            'We are at 444 Weber Street',
            'steak bread hot dog',
            '888 Socks Drive',
            'chicken broccoli lol',
            '8 oz steak',
            'turkey club',
            "2:00 pm"
        }
        for item in testingSet:
            result = self.classify(item)
            print "%s | %s | %s" % (item, result[0], result[1])
