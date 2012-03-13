# Routines to grab some bits of data from the chec data.  The front end will randomly 

from string import Template
from webapp2_extras import json

class Inspiration:
    """This class picks a bunch of data out of the retrieved checkin data with 
    an eye to coming up with possible search terms to use to build a playlist from."""
    
    # This is kind of clunky, but keeping the dict seperate makes the 
    # JSON serialization trivial
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
        clean = []
        
        # This is sort of a desultory effort but I'm not convinced 
        # that these cleanups will actually result in cleaner searches
        for word in address.split(None):
            lower = word.lower()
            
            # Some things we just nuke
            if lower == 'at': continue
            elif lower == 'btw': continue
            elif lower == 'btwn': continue
            elif word.isdigit(): continue
            
            # Or we make substitiutions
            elif lower == 'st' or lower == 'st.':
                word = 'Street'
            elif lower == 'ave' or lower == 'ave.':
                word = 'Avenue'
            elif lower == 'pl' or lower == 'pl.':
                word = 'Place'
            elif lower == 'n': word = 'North'
            elif lower == 'e': word = 'East'
            elif lower == 's': word = 'South'
            elif lower == 'w': word = 'West'
            
            clean.append(word)
        return ' '.join(clean) 

    def to_dict(self): 
        return self._dict
    
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
