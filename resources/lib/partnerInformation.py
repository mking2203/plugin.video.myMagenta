import json

class partnerInformation(object):

    # nur ein object
    name = ''
    rentPrice = 0
    buyPrice = 0
    launchUrl = ''

    def __init__(self, data):
        self.jData = data

        if 'name' in self.jData: self.name = self.jData['name']
        if 'rentPrice' in self.jData: self.rentPrice = self.jData['rentPrice']
        if 'buyPrice' in self.jData: self.buyPrice = self.jData['buyPrice']
        if 'launchUrl' in self.jData: self.launchUrl = self.jData['launchUrl']['href']



