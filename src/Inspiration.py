# Routines to grab random bits of checkin data in order to form a playlist

from string import Template
from webapp2_extras import json

class Inspiration:
    def __init__(self, checkin):
        venue = checkin['venue']
        d = {}
        
        d[u'venueName'] = venue['name']
        
        for category in venue['categories']:
            if category['primary']:
                d[u'categoryName'] = category['name']
        
        loc = venue['location']
        d[u'street'] = self._cleanupAddress(loc['address'])
        
        if 'crossStreet' in loc:
            d[u'crossStreet'] = self._cleanupAddress(loc['crossStreet'])
        d[u'city'] = loc['city']
        d[u'country'] = loc['country']
        d[u'state'] = self._getUsState(loc['state'])
        
        self._dict = d
    
    def _getUsState(self, abbr):
        """If abbr is a state abbreviation, return the full name. Else return 
        the abbreviation."""
        return unicode(_all_states.get(abbr, abbr))
    
    def _cleanupAddress(self, address):
        """Given a street address, clean it up to make it more suitable for a song title"""
        return address

    def to_dict(self): 
        return dict([(key, self._dict[key]) for key in self._dict.keys()])
    
    def __repr__(self):
        #return json.encode(self._dict, ensure_ascii=False))
        return str(self._dict)


def find(checkinList):
    """Return a list of one Inspiration object per checkin."""
    return [Inspiration(item) for item in checkinList]

# snagged from http://code.activestate.com/recipes/577305/ (r1), MIT License
_all_states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming',
        # Those crazy canucks
        'AB': 'Alberta',
        'BC': 'British Columbia',
        'MB': 'Manitoba',
        'NB': 'New Brunswick',
        'NL': 'Newfoundland and Labrador',
        'NT': 'Northwest Territories',
        'NS': 'Nova Scotia',
        'NU': 'Nunavut',
        'ON': 'Ontario',
        'PE': 'Prince Edward Island',
        'QC': 'Quebec',
        'SK': 'Saskatchewan',
        'YT': 'Yukon'
}
