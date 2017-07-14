# Publications Query

This project provides a Python script which lets the SAAO librarians search ADS for articles related to the SAAO and SALT. It does this in three ways.

* Perform a full text search in ADS for a set of keywords.
* Search for publications with the SAAO or SALT as an affiliation.
* Search for publications with an author from a list of authors.

The results are collected in a spreadsheet and sent by email to the librarians.

## Requirements

The following requirements must be met for this project.

* Python 3.5 or higher must be installed.
* The Python libraries in `requirements.txt` must be installed.
* You need an API key for the ADS (see the section on configuration below).

## Installation

The easiest way to install the project is to clone it onto your machine.

```bash
git clone git@bitbucket.org:hettlage/saao-publications-query.git
```

Finally, you need to add a configuration file, as explained in the following section. 

## Configuration

You need to create a file `python/config.py` and define the following constants in it.

| Constant | Description | Example |
| -- | -- | -- |
| `ADS_API_KEY` | API key for ADS | `'IbjwNBx4Wn6uxpQK56m0q14lO6wvRaCwBC4sYfNV'` |
| `AUTHORS` | Dictionary of authors to search for and their email addresses | `{'Buckley, D': ''David Buckley <dibnob@saao.ac.za>', 'Mohammed, S': 'Shazrene Mohammed <shazrene@saao.ac.za>'}` |
| FROM_EMAIL_ADDRESS | Email address to use in the From field | `library@saao.ac.za` |
| `KEYWORDS` | Array of keywords to search for | `['SAAO', 'KELT', 'Infrared Survey'] ` |
| `LIBRARIAN_EMAIL_ADDRESSES` | Array of the librarians' email addresses | `['Theresa de Young <theresa@saao.ac.za>', 'Zuthobeke Mvakade <zm@saao.ac.za>']` |

The keys of the dictionary of authors must be given as *Last Name, First Name Other Initials* (example: *Potter, Stephen* or *Potter, Stephen B*), as you would expect for an ADS query (see [http://adsabs.github.io/help/search/search-syntax](http://adsabs.github.io/help/search/search-syntax). The corresponding values should be of the form *first name last name &lt;address&gt;*.

The email addresses of the librarians should be given as *first name last name &lt;address&gt;*.

The API key for ADS can be obtained from [https://ui.adsabs.harvard.edu/](https://ui.adsabs.harvard.edu/). You  need to log in, choose 'Customize Settings' from the Account menu and then select 'API Token' from the menu. The API key for Science Direct can be obtained from [http://dev.elsevier.com](http://dev.elsevier.com). 

You shouldn't include the API keys in the configuration file, but rather set them by means of environment variables:

```python
import os
ADS_API_KEY = os.environ['ADS_API_KEY']
SCIENCE_DIRECT_API_KEY = os.environ['SCIENCE_DIRECT_API_KEY']
```

Here is an example of what the configuration file might look like.

```python
import os

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

# email addresses of the librarians
LIBRARIAN_EMAIL_ADDRESSES = [
    'Theresa de Young <theresa@saao.ac.za>',
    'Zuthobeke Mvakade <zm@saao.ac.za>'
]

ADS_API_KEY = os.environ['ADS_API_KEY']
```

## Architecture

The Python script uses the [ads](https://github.com/andycasey/ads) library for performing the ADS queries. Its requirements are handled with `pip`, and the requirements are listed in the file `requirements.txt`.
