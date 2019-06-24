import json

class contentInformation(object):

    # nur ein object
    ID = 0
    title = 'Unbekannt'
    originalTitle = ''
    genre = 'Unbekannt'
    description = ''
    longDescription = None
    metaData = ''
    year = None
    runtime = None
    country = 'Unbekannt'
    detailPage = ''
    childProtection = 'Unbekannt'
    communityRating = None
    assetOrdinal = 0

    def __init__(self, data):
        self.jData = data

        if 'id' in self.jData: self.ID = self.jData['id']
        if 'title' in self.jData: self.title = self.jData['title']
        if 'description' in self.jData: self.description = self.jData['description']
        if 'mainGenre' in self.jData: self.genre = self.jData['mainGenre']
        if 'year' in self.jData: self.year = self.jData['year']
        if 'runtime' in self.jData: self.runtime = self.jData['runtime']
        if 'countries' in self.jData:
            if len(self.jData['countries']) > 0: self.country = self.jData['countries'][0]
        if 'detailPage' in self.jData: self.detailPage = self.jData['detailPage']['href']
        if 'longDescription' in self.jData: self.longDescription = self.jData['longDescription']
        if 'orgTitle' in self.jData: self.originalTitle = self.jData['orgTitle']
        if 'childProtectionDisplayName' in self.jData: self.childProtection = self.jData['childProtectionDisplayName']
        if 'communityRatingStars' in self.jData: self.communityRating = self.jData['communityRatingStars']
        if 'assetOrdinal' in self.jData: self.assetOrdinal = self.jData['assetOrdinal']
        if 'metaData' in self.jData: self.metaData = self.jData['metaData']

    def getImages(self):
        if 'images' in self.jData:
            return self.jData['images']
        else:
            return []

    def getCast(self):
        if 'castAndCrew' in self.jData:
            return self.jData['castAndCrew']
        else:
            return []

    def getTrailer(self):
        if 'trailers' in self.jData:
            trs = self.jData['trailers']
            if len(trs)>0:
                return self.jData['trailers'][0]['href']
            else:
                return None
        else:
            return None

