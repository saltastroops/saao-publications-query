import os

from dotenv import load_dotenv

load_dotenv()

ADS_API_KEY = os.getenv('ADS_API_KEY')

WOS_API_KEY = os.getenv('WOS_API_KEY')

LIBRARIAN_EMAIL_ADDRESSES = os.getenv('LIBRARIAN_EMAIL_ADDRESSES').strip('][').split(', ')

FROM_EMAIL_ADDRESS = os.getenv('FROM_EMAIL_ADDRESS')

# keywords to search for
KEYWORDS = [
    'KELT',
    'Infrared Survey'
]

# authors to search for and their email addresses
AUTHORS = {
    'Skelton, R': 'Ros Skelton <ros@saao.ac.za>',
    'Kniazev, A': 'Alexei Kniazev <akniazev@saao.ac.za~'
}

AFFILIATIONS = [
    'South African Large Telescope'
]

# Institutions to search for. Each institution must be in the list of affiliations used by the ADS
# (https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv),
# and its name must be given exactly as in that list.
INSTITUTIONS = [
    'SAAO'
]

SALT_PARTNERS = [
    'Georg-August-Universität Göttingen',
    'University of Wisconsin-Madison',
    'University of North Carolina - Chapel Hill',
    'Dartmouth College',
    'Rutgers University',
    'Carnegie Mellon University',
    'University of Canterbury',
    'Inter-University Centre for Astronomy & Astrophysics',
    'Durham University'
]

EXCLUDED_JOURNALS = ['']