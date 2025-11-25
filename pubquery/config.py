import json
import os
from json import JSONDecodeError

from dotenv import load_dotenv

load_dotenv()

ADS_API_KEY = os.getenv("ADS_API_KEY")

WOS_API_KEY = os.getenv("WOS_API_KEY")

SMTP_SERVER = os.getenv("SMTP_SERVER")

SMTP_PORT = os.getenv("SMTP_PORT")

try:
    LIBRARIAN_EMAIL_ADDRESSES = json.loads(os.getenv("LIBRARIAN_EMAIL_ADDRESSES"))
except JSONDecodeError:
    raise ValueError(
        "The value of the LIBRARIAN_EMAIL_ADDRESSES environment variable "
        "must be a list of double-quoted strings. For example: "
        '["John Doe <john@example.com>", '
        '"Jane Miller <jane@example.com>"]'
    )

FROM_EMAIL_ADDRESS = os.getenv("FROM_EMAIL_ADDRESS")

# keywords to search for
KEYWORDS = [
    "SAAO",
    "SALT",
    "South African Astronomical Observatory",
    "Southern African Large Telescope",
    "African Large Telescope",
    "African Astronomical Observatory",
    "IRSF",
    "MONET",
    "BiSON",
    "SuperWASP",
    "KELT",
    "LCOGT SAAO",
    "LCOGT Sutherland",
    "KMTNeT",
    "MASTER SAAO",
    "MASTER",
    "Meerlicht",
    "Solaris",
    "Infrared Survey Facility",
    "Las Cumbres Observatory Global Telescope",
    "SHOC",
    "Sutherland high-speed optical camera",
    "HIPPO",
    "SpCCD",
    "WALOP",
    "ste3",
    "ste4",
    "salticam",
    "maxiE",
    "robopol",
    "ATLAS",
    "ATLAS-SOUTH",
    "PRIME",
    "ASTMON",
    "SANSA/DLR/SMARTNet",
    "ACT/APT",
    "Asteroid Terrestrial Impact Last Alert System",
    "WFTC II",
    "Wide Field Cryogenic Telescope",
    "OCR",
    "Optical Space Research",
    "ASAS-SN",
    "Allsky Automated Survey for Supernovae",
    "Xamidimura",
    "SAGOS",
    "South African Geodynamic Observatory",
    "ASTMON",
    "PRIME",
    "PRime Focus Infrared Microlensing Experiment",
]

# authors to search for and their email addresses
AUTHORS = {
    'Doe, Jane': 'Jane Doe <doe@example.com',
    'Else, Someone': 'Someone Else <someone@sexample.com>'
}

AFFILIATIONS = [
    "South African Astronomical Observatory",
    "Southern African Large Telescope",
]

# Institutions to search for. Each institution must be in the list of affiliations used by the ADS
# (https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv),
# and its name must be given exactly as in that list.
INSTITUTIONS = ["SAAO"]

SALT_PARTNERS = [
    "Georg-August-Universität Göttingen",
    "University of Wisconsin-Madison",
    "University of North Carolina - Chapel Hill",
    "Dartmouth College",
    "Rutgers University",
    "Carnegie Mellon University",
    "University of Canterbury",
    "Inter-University Centre for Astronomy & Astrophysics",
    "Durham University",
]

EXCLUDED_JOURNALS = [
    "Advances in space research",
    "Dynamics of atmospheres and oceans",
    "Earth and planetary science letters",
    "Geochimica et Cosmochimica Acta",
    "Geophysical research letters",
    "International journal of astrobiology",
    "Journal of Advances in Modeling Earth Systems",
    "Journal of geophysical research",
    "Journal of geophysical research (planets)",
    "Journal of geophysical research (space physics)",
    "Journal of high energy physics",
    "Life sciences and space research",
    "LPI Contributions",
    "Physics of the earth and planetary interiors",
    "The planetary science journal",
    "Space science reviews",
]
