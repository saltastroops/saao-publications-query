# Publications Query

This project provides a Python script which lets the SAAO librarians search ADS for articles related to the SAAO and SALT. It does this in three ways.

* Perform a full text search in ADS for a set of keywords.
* Search for publications with the SAAO or SALT as an affiliation.
* Search for publications with an author from a list of authors.

The results are collected in a spreadsheet and sent by email to the librarians.

## Requirements

The following requirements must be met for this project.

* Python 3.13 or higher must be installed (although you might get away with a slightly older version, in which case you should update the `requires-python` value in `pyproject.toml`).
* * You need an API key for the ADS and an API key for the Web of Science. See below for instructions.

## Running the script

To run the script, first clone the project repository:

```bash
git clone git@github.com:saltastroops/saao-publications-query.git
```

Then change into the project directory:

```bash
cd saao-publications-query
```

Update the configuration file `pubquery/config.py` as described in the section `Configuration` below.

The easiest way to launch the script is to use [uv](https://docs.astral.sh/uv/):

```bash
uv run pubquery/publications_query.py --start 2025-11-01 --end 2025-11-30
```

If you don't want to use uv, you have to install the script and its dependencies with pip in a virtual environment first:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python pubquery/publications_query.py --start 2025-11-01 --end 2025-11-30
```

The script requires the following options:

| Option    | Alias | Description                                                                                              | Example |
| --- | --- | --- | --- |
| `--start` | `-s`  | The start date, in the form yyyy-mm-dd. A full date must be given, but only the year and month are used. | `2025-11-01` |
`--end` | `-e` | The end date, in the form yyyy-mm-dd. A full date must be given, but only the year and month are used. | `2025-11-01` |

Both the start date and end date are inclusive. So, for example, if the start date is 1 November 2025 and the end date is 1 December 2025, both November and December are queried.

## Configuration

You need to update the file `pubquery/config.py` and define the following constants in it.

| Constant | Description                                                                                                                                                                                                                          | Example                                                                                      |
| -- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|
| `AFFILIATIONS` | Author affiliations to query for                                                                                                                                                                                                     | `["South African Astronomical Observatory", "Southern African Large Telescope"]`             |
| `ADS_API_KEY` | API key for ADS                                                                                                                                                                                                                      | `topsecretapikeu`                                                                            |
| `AUTHORS` | Dictionary of authors to search for and their email addresses                                                                                                                                                                        | `{"Buckley, D": "David Buckley <dibnob@saao.ac.za>", "Mohammed, S": "Shazrene Mohammed <shazrene@saao.ac.za>"}` |
| `EXCLUDED_JOURNALS` | Journals whose articles should not be included in query results | `["Geochimica et Cosmochimica Acta", "Geophysical research letters"]`                        |
| `FROM_EMAIL_ADDRESS` | Email address to use in the From field                                                                                                                                                                                               | `library@saao.ac.za`                                                                         |
| `INSTITUTIONS` | Instititutions to query for. Each institution must be in the [list of affiliations used by the ADS](https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv), and its name must be given exactly as in that list | `["SAAO"]`                                                                                   |
| `KEYWORDS` | Array of keywords to search for                                                                                                                                                                                                      | `["SAAO", "KELT", "Infrared Survey"] `                                                       |
| `LIBRARIAN_EMAIL_ADDRESSES` | Array of the librarians' email addresses                                                                                                                                                                                             | `["Jane Miller <jane@example.org>", "Siphelo Dlama <siphelo@example.org>"]`                  |
| `SALT_PARTNERS` | List of SALT partners                                                                                                                                                                                                                | `["Dartmouth", "Rutgers"]`                                                                   |
| `SMTP_PORT` | Port on which the SMTP server is listening | `25` |
| `SMTP_SERVER` | SMTP server to use for sending emails | `smtp.example.org` |
| `WOS_API_KEY` | API key for the Web of Science                                                                                                                                                                                                       | `topsecretapikey`                                                                            |

The keys of the dictionary of authors must be given as *Last Name, First Name Other Initials* (example: *Potter, Stephen* or *Potter, Stephen B*), as you would expect for an ADS query (see [http://adsabs.github.io/help/search/search-syntax](http://adsabs.github.io/help/search/search-syntax). The corresponding values should be of the form *first name last name &lt;address&gt;*.

The email addresses of the librarians should be given as *first name last name &lt;address&gt;*.

The API key for ADS can be obtained from [https://ui.adsabs.harvard.edu/](https://ui.adsabs.harvard.edu/). You need to log in, choose 'Customize Settings' from the Account menu and then select 'API Token' from the menu. The API key for the Web of Science (Elseviewr Direct) can be obtained from [http://dev.elsevier.com](http://dev.elsevier.com). 

You can use environment variables in the configuration file, which may be defined in a `.env` file in the project root folder. This is particularly recommended for confidential information such as API keys. Make sure the `.env` file is *not* under version control.

## Architecture

The Python script uses the [ads](https://github.com/andycasey/ads) library for performing the ADS queries.
