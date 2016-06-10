# Publications Query

This project provides a Python and a Java script which together let the SAAO librarians search ADS for articles related to the SAAO and SALT. It does this in four ways.

* Query for all publications in a list of journals, download the pdf files and perform a full text search for a set of keywords in these files.
* Perform a full text search in ADS for a set of keywords.
* Search for publications with the SAAO or SALT as an affiliation.
* Search for publications with an author from a list of authors.

The results are collected in a spreadsheet and sent by email to the librarians.

# Configuration

The following constants need to be defined in the file `config.py`.

| Constant | Description | Example |
| == | == | == |
| `JOURNALS` | Array of bibcode abbreviations of journals to query | `['ApJ', 'MNRAS'] |
| `KEYWORDS` | Array of keywords to search for | `['SAAO', 'KELT', 'Infrared Survey'] ` |
| `AUTHORS` | Array of authors to search for | `['Buckley, D', 'Mohammed, S', 'Skelton, R']` |
| `LIBRARIAN_EMAIL_ADDRESSES` | Array of the librarians' email addresses | `['Theresa de Young <theresa@saao.ac.za>', 'Zuthobeke Mvakade <zm@saao.ac.za>']` |
| `SCIENCE_DIRECT_API_KEY` | API key for the Science Direct API | `'71ec82719aed381f6c2z8d42f186ac8f'` |

The journal abbreviations must be the ones used for the ADS bibcodes. 

The keywords are case-sensitive for the pdf search; if the keyword is 'Infrared Survey', the string 'infrared survey' won't be picked up. They are found even if they form part of a word. For example, 'shoc' would be found in the string 'the speed of the shock front'.

The authors must be given as *Last Name, Initial*, as you would expect for an ADS query.

The email addresses of the librarians should be given as *first name last name <address>*.

The API key for Science Direct can be obtained from [http://dev.elsevier.com](http://dev.elsevier.com). You shouldn't include it in the configuration file, but rather set it by means of an environment variable:

```python
import os
SCIENCE_DIRECT_API_KEY = os.environ['SCIENCE_DIRECT_API_KEY']
```

Here is an example of what the configuration file might look like.

