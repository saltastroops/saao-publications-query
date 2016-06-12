import os

# ADS bibcode abbreviations of journals to query
JOURNALS = [
    'A&A',
    'A&ARv',
    'AJ',
    'AN',
    'ARA&A',
    'ARep',
    'Afz',
    'Ap',
    'Ap&SS',
    'ApJ',
    'AstL',
    'Icar',
    'MNRAS',
    'NATUR',
    'NewA',
    'NewAR',
    'PASJ',
    'PASP'
]

# keyword to search for
KEYWORDS = [
    'KELT',
    'Infrared Survey'
]

# authors to search for and their email addresses
AUTHORS = {
    'Skelton, R': 'Ros Skelton <ros@saao.ac.za>',
    'Kniazev, A': 'Alexei Kniazev <akniazev@saao.ac.za~'
}

# email addresses of the librarians
LIBRARIAN_EMAIL_ADDRESSES = [
    'Theresa de Young <theresa@saao.ac.za>',
    'Zuthobeke Mvakade <zm@saao.ac.za>'
]

ADS_API_KEY = os.environ['ADS_API_KEY']

SCIENCE_DIRECT_API_KEY = os.environ['SCIENCE_DIRECT_API_KEY']

OUTPUT_DIR = '/Users/christian/Desktop/PUBLICATIONS'
