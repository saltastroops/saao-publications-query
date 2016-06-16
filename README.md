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
* Apache Maven 3.3.9 or higher must be installed.
* You need API keys for the ADS and Science Direct (see the section on configuration below).

## Installation

The easiest way to install the project is to clone it onto your machine.

```bash
git clone git@bitbucket.org:hettlage/saao-publications-query.git
```

After cloning the repository and after pulling changes you should use Maven to package the Java program.

```bash
cd java
mvn package
```

Finally, you need to add a configuration file, as explained in the following section. 

## Configuration

You need to copy the file `python/config.example.py` to `python/config.py` and define the following constants in it.

| Constant | Description | Example |
| -- | -- | -- |
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

```python
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
    'AstL',
    'Icar',
    'MNRAS',
    'NATUR',
    'NewA',
    'NewAR',
    'PASJ',
    'PASP'
]

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

SCIENCE_DIRECT_API_KEY = os.environ['SCIENCE_DIRECT_API_KEY']

OUTPUT_DIR = '/Users/christian/Desktop/PUBLICATIONS'
```

## Architecture

The project consists of a Python script and a Java program. The role of the Python script is to carry out all the queries to ADS, download the PDF files, initiate the keyword search, put together spreadsheets with the results and finally send out emails.

The sole responsibility of the Java program is to search for the keywords in the downloaded PDF files. This part isn't realised in Python, as the parsing of PDF files is faster in Java by one or two orders of magnitude.

The Python script calls the Java program by running a subprocess. The paths to the PDF files and the keywords are passed as a JSON object to the stdin stream of the Java program.

```json
{
    "pdfs": ["/path/to/file1", "/path/to/file2", ..., "/path/to/fileN"],
    "keywords": ["keyword1", "keyword2", ..., "keywordN"]
 }
```

The results of the keyword search are passed back to the Python script as a JSON object via the Java program's stdout stream.

```json
{
    "results": [
        {
            "pdf": "/path/to/file1",
            "keywords": ["keyword3", "keyword7"]
        },
        {
            "pdf": "/path/to/file2",
            "keywords": []
        },
        {
            "pdf": "/path/to/file3",
            "keywords": null
        }
    ]
}
```

`null` is used as the value for the keywords if the keyword search couldn't be executed for the corresponding PDF.

The Python script uses the [ads](https://github.com/andycasey/ads) library for performing the ADS queries. Its requirements are handled with `pip`, and the requirements are listed in the file `requirements.txt`.

The Java program uses the [itextpdf](http://itextpdf.com) library for parsing the PDF files. It is contained in a Maven project.         
    
