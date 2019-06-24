import json

class channel:

    number = ''
    name =''
    picture = ''

class channels(object):

    def __init__(self, data):
        self.jData = data

    def getChannel(self, channelNo):

        ch = channel
        ch.name = 'Channel %s' % str(channelNo)

        for item in self.jData['channellist']:
            if item['contentId'] == str(channelNo):
                ch.name = item['name']
                ch.number = item ['chanNo']

                # just take first picture
                pics = item ['pictures']
                for p in pics:
                    ch.picture = p['href']
                    break

        return ch



