# Publications Query

This project provides a Python and a Java script which together let the SAAO librarians search ADS for articles related to the SAAO and SALT. It does this in four ways.

* Query for all publications in a list of journals, download the pdf files and perform a full text search for a set of keywords in these files.
* Perform a full text search in ADS for a set of keywords.
* Search for publications with the SAAO or SALT as an affiliation.
* Search for publications with an author from a list of authors.

The results are collected in a spreadsheet and sent by email to the librarians.

## Requirements

The following requirements must be met for this project.

* Python 3.5 or higher must be installed.
* The Python libraries in `requirements.txt` must be installed.
* Java 1.8 ("Java 8") or higher must be installed.
* You need API keys for the ADS and Science Direct (see the section on configuration below).

## Configuration

You need to copy the file `python/config.example.py` to `python/config.py` and define the following constants in it.

| Constant | Description | Example |
| == | == | == |
| `JOURNALS` | Array of bibcode abbreviations of journals to query | `['ApJ', 'MNRAS']` |
| `KEYWORDS` | Array of keywords to search for | `['SAAO', 'KELT', 'Infrared Survey'] ` |
| `AUTHORS` | Dictionary of authors to search for and their email addresses | `{'Buckley, D': ''David Buckley <dibnob@saao.ac.za>', 'Mohammed, S': 'Shazrene Mohammed <shazrene@saao.ac.za>'}` |
| `LIBRARIAN_EMAIL_ADDRESSES` | Array of the librarians' email addresses | `['Theresa de Young <theresa@saao.ac.za>', 'Zuthobeke Mvakade <zm@saao.ac.za>']` |
| `ADS_API_KEY` | API key for ADS | `'IbjwNBx4Wn6uxpQK56m0q14lO6wvRaCwBC4sYfNV'` |
| `SCIENCE_DIRECT_API_KEY` | API key for Science Direct | `'71ec82719aed381f6c2z8d42f186ac8f'` | 
| `OUTPUT_DIR` | Directory for the generated files | `'/path/to/output/dir'` |

The journal abbreviations must be the ones used for the ADS bibcodes. 

The keywords are case-sensitive for the pdf search; if the keyword is 'Infrared Survey', the string 'infrared survey' won't be picked up. They are found even if they form part of a word. For example, 'shoc' would be found in the string 'the speed of the shock front'.

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

