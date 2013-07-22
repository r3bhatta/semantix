import re
import collections

"""
From a list of labels and their frequencies, retrieve the label with highest frequency and the
average probability of that label.
"""
def highestFrequency(labels):
    frequencies = {}
    # Go through labels and create a frequency map.
    for label in labels:
        if label[0] not in frequencies:
            frequencies[label[0]] = {'frequency': 1, 'probabilities': [label[1]]}
        else:
            frequencies[label[0]]['frequency'] += 1
            # Accumulate a list of probabilities.
            frequencies[label[0]]['probabilities'].append(label[1])
    
    # Get the result with highest frequency and calculate its average probability.
    result = []
    highest = 0
    for label in frequencies:
        frequency = frequencies[label]['frequency']
        if frequency > highest:
            highest = frequency
            # Calculate average probability.
            averageProbability = 0
            for probability in frequencies[label]['probabilities']:
                averageProbability += probability
            averageProbability /= frequency

            return {'label': label, 'probability': averageProbability}
    """
    # For testing.
    for label in frequencies:
        print '%s | %s' % (label, frequencies[label]['frequency'])
    """
    return result

"""
Get the business type of the business file.
"""
def parseBusinessType(businessFile, soups, nbc):
    labels = []
    for soup in soups:
        labels.append(nbc.classify(soup.getText()))

    businessType = collections.namedtuple('BusinessType', \
            ['file', 'label', 'probability'])
    label = highestFrequency(labels)

    return businessType(businessFile, label['label'], label['probability'])

