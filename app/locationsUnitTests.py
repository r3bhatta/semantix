import stringSimilarity

def filterDuplicateAddresses():
    filteredAddresses = []
    for address1 in addresses[:]:
        if address1 not in addresses:
            break
        addresses.remove(address1)
        for address2 in addresses[:]:
            similarity = stringSimilarity.compute(address1, address2)
            if similarity > 0.6:
                addresses.remove(address2)
                if len(address2) > len(address1):
                    address1 = address2
        filteredAddresses.append(address1)
    return filteredAddresses

addresses = ["123 fake", "123 fake st", "123 fake st kitchener", "123 fake st kitchener, ontario", "123 fake st kitchener, ontario st", "123 fake", "123 fake st"]

print filterDuplicateAddresses()