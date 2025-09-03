# Publications Query

This project provides a Python script which lets the SAAO librarians search ADS for articles related to the SAAO and SALT. It does this in three ways.

* Perform a full text search in ADS for a set of keywords.
* Search for publications with the SAAO or SALT as an affiliation.
* Search for publications with an author from a list of authors.

The results are collected in a spreadsheet and sent by email to the librarians.

## Requirements

The following requirements must be met for this project.

* A recent version of Python 3 must be installed.
* The Python libraries in `requirements.txt` must be installed.
* You need an API key for the ADS and an API key for the Web of Science (see the section on configuration below).

## Installation

The easiest way to install the project is to clone it onto your machine.

```bash
git clone git@github.com:saltastroops/saao-publications-query.git
```

Finally, you need to add a configuration file, as explained in the following section. 

## Configuration

You need to create a file `.env` and define the following constants in it.

| Constant | Description | Example                                                                                                         |
| -- | -- |-----------------------------------------------------------------------------------------------------------------|
| `ADS_API_KEY` | API key for ADS | `topsecretadskey`                                                                                               |
| `WOS_API_KEY` | API key for Web of Science | `topsecretwoskey`                                                                                               |
| `AUTHORS` | Dictionary of authors to search for and their email addresses | `{'Longman, P': 'Peter Longman <peter@example.org>', 'Mohammed, S': 'Shazrene Mohammed <shazrene@example.org>'}` |
| `FROM_EMAIL_ADDRESS` | Email address to use in the From field | `library@example.org`                                                                                           |
| `KEYWORDS` | Array of keywords to search for | `['SAAO', 'KELT', 'Infrared Survey'] `                                                                          |
| `LIBRARIAN_EMAIL_ADDRESSES` | Array of the librarians' email addresses | `['Jane Doe <jane@example.org>', 'Peter Miller <peter@example.org>']`                                           |

The keys of the dictionary of authors must be given as *Last Name, First Name Other Initials* (example: *Potter, Stephen* or *Potter, Stephen B*), as you would expect for an ADS query (see [http://adsabs.github.io/help/search/search-syntax](http://adsabs.github.io/help/search/search-syntax). The corresponding values should be of the form *first name last name &lt;address&gt;*.

The email addresses of the librarians should be given as *first name last name &lt;address&gt;*.

The API key for ADS can be obtained from [https://ui.adsabs.harvard.edu/](https://ui.adsabs.harvard.edu/). You  need to log in, choose 'Customize Settings' from the Account menu and then select 'API Token' from the menu.
