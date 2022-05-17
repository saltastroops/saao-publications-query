import collections
import datetime
import io
import os
import re
import smtplib
import sys
import time
import xlsxwriter
import requests
import json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote

import config
from ads_queries import ADSQueries
from wos_queries import WoSQueries


def ignore_tmp_bibcodes(bibcodes):
    """Filter out bibcodes which are temporary.

    Params
    -------
    bibcodes : list of str
        Bibcodes to filter.

    Returns
    -------
    list of str
        List of bibcodes lswithout the temporary ones.
    """

    return [bibcode for bibcode in bibcodes if 'tmp' not in bibcode]


def previously_found_bibcodes():
    """Return the list of bibcodes found in previous searches.

    The previously found publications are stored as bibcode in a file, whose path is set as PREVIOUS_BIBCODES_FILE in
    the configuration file. If this file doesn't exist, it is created first. If it cannot be created, an exception is
    raised.

    Returns
    -------
    list
        List of publications found in a previous search.
    """

    # create the file for storing previously found bibcodes, if need be
    _ensure_previously_recorded_file_exists()

    with open(config.PREVIOUS_BIBCODES_FILE) as f:
        return [line.strip() for line in f.readlines()]


def _ensure_previously_recorded_file_exists():
    """Create the file for storing previously found bibcodes, if it doesn't exist yet.

    If the file cannot be created an exception is raised.
    """

    if not os.path.isfile(config.PREVIOUS_BIBCODES_FILE):
        with open(config.PREVIOUS_BIBCODES_FILE, 'w') as f:
            f.close()

    # check whether the file could be created
    if not os.path.isfile(config.PREVIOUS_BIBCODES_FILE):
        raise IOError('The file for storing previously found bibcodes could not be created: ' +
                      config.PREVIOUS_BIBCODES_FILE)


def publications_spreadsheet(publications, columns):
    """Create a spreadsheet with the publications.

    Params
    ------
    publications : list
        Publications.
    columns : list of str
        Columns to include in the spreadsheet.

    Returns
    -------
    io.BytesIO
        Spreadsheet with the publication details.

    """
    out = io.BytesIO()
    workbook = xlsxwriter.Workbook(out)

    worksheet = workbook.add_worksheet()
    for row, p in enumerate(publications):
        for col, c in enumerate(columns):
            worksheet.write(row, col, p.get(c, ''))

    workbook.close()

    # rewind the buffer
    out.seek(0)

    return out


def spreadsheet_columns():
    """Return an ordered dictionary of the columns for a spreadsheet.

    The dictionary keys are the keys to use for accessing details in a publication dictionary, the values are more
    human-friendly column names.

    Some keys may not be included in a publication dictionary.

    Returns
    -------
    collections.OrderedDict
        Dictionary of column keys and names.
    """
    columns = collections.OrderedDict()
    columns['record_type'] = 'Record Type'
    columns['publication_number'] = 'Doc/Publication Number'
    columns['author'] = 'Responsibility'
    columns['institute_of_first_author'] = 'Institute of first author'
    columns['title'] = 'Title'
    columns['pub'] = 'Journal'
    columns['pubdate'] = 'Publication date (YYYY-MM-DD)'
    columns['volume'] = 'Volume'
    columns['issue'] = 'Issue'
    columns['page'] = 'Page'
    columns['refereed'] = 'Refereed'
    columns['bibcode'] = 'Bibcode'
    columns['doi'] = 'DOI'
    columns['ads_url'] = 'ADS URL'
    columns['doi_in_wos'] = 'DOI in WoS'
    columns['abstract'] = 'Abstract'
    columns['telescopes'] = 'Telescopes'
    columns['fulltext_keywords'] = 'Keywords found in full text '
    columns['keyword'] = 'Keywords found in the abstract'
    columns['aff'] = 'Authors\' affiliation'
    columns['SALT_partners'] = 'SALT partner institutions'
    columns['SA_institutions'] = 'South African institutions'
    columns['no_of_authors_aff_to_SA_ins'] = 'No. of authors on paper affiliated to a SA institution'
    columns['authors_affiliated_with_SAAO'] = 'Authors affiliated with SAAO'

    return columns


def send_mails(spreadsheets, columns):
    column_explanation = '\n'.join([chr(ord('A') + i) + ' - ' + columns[key] + '<br>'
                                    for i, key in enumerate(columns.keys())])

    outer = MIMEMultipart()
    outer['Subject'] = 'Publications Query Results'
    outer['To'] = config.LIBRARIAN_EMAIL_ADDRESSES
    outer['From'] = config.FROM_EMAIL_ADDRESS
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    body = MIMEMultipart('alternative')
    html = '''<p>Dear Librarian,</p>

<p>Please find attached the results for the publications query.</p>

<p>{column_explanation}</p>

<p>Kind regards,</p>

<p>Your Friendly Publications Query Script</p>'''.format(column_explanation=column_explanation)
    text = re.sub('<[^>]+>', '', html)

    body.attach(MIMEText(text, 'plain'))
    body.attach(MIMEText(html, 'html'))

    outer.attach(body)

    for spreadsheet in spreadsheets:
        msg = MIMEBase('application', 'application/vnd.ms-excel')
        read = spreadsheet['content'].read()
        msg.set_payload(read)
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=spreadsheet['name'])
        outer.attach(msg)

    with smtplib.SMTP('smtp.saao.ac.za') as s:
        s.sendmail(config.FROM_EMAIL_ADDRESS, ', '.join(config.LIBRARIAN_EMAIL_ADDRESSES), outer.as_string())


def get_authors_and_affiliations(publication):
    """Return lists of authors and affiliations of a given publication.

    Params
    ------
    publication: publication dictionary

    Returns
    -------
    lists
        Lists of authors and affiliations.
    """
    # query authors and affiliations
    url_template = 'https://ui.adsabs.harvard.edu/v1/search/query?{}'
    query_params = {'fl': 'aff, author', 'q': 'identifier:{0}'.format(publication['bibcode']), 'rows': 1}
    query_url = url_template.format(urlencode(query_params, quote_via=quote))

    max_retries = 3
    retries = 0
    while retries <= max_retries:
        try:
            response = requests.get(query_url, headers={'Authorization': 'Bearer ' + config.ADS_API_KEY})
            response.raise_for_status()
            break
        except requests.exceptions.HTTPError:
            print("Retrying...")
            retries += 1
            if retries > max_retries:
                raise

    soup = BeautifulSoup(response.text, 'html.parser')
    content = json.loads(soup.text)
    query_result = content['response']['docs'][0]

    publication['author'] = ', '.join(query_result['author'])
    publication['aff'] = '| '.join(query_result['aff'])

    return query_result['author'], query_result['aff']


def check_doi_indexed_in_wos(publication):
    # check whether the DOI is indexed in the Web of Science (WoS)
    doi = publication['doi'][0] if publication['doi'] and len(publication['doi']) > 0 else None
    publication['doi_in_wos'] = wos_queries.is_doi_indexed(doi).value


def get_south_african_affiliations(affiliations):
    """Return string of South African institutions in a publication.

    Params
    ------
    affiliations : list of affiliations in a publication separated by a semicolon

    Returns
    -------
    str
        South African institutions separated by '|'.
    """
    south_african_affiliations = []
    for k, affiliation in enumerate(affiliations.split('; ')):
        # add South African institutions
        if "South Africa" in affiliation:
            south_african_affiliations.append(affiliation)
    return south_african_affiliations


def get_salt_partners(affiliations):
    """Return string of South African Large Telescope (SALT) partner institutions in a publication.

    Params
    ------
    affiliations : list of affiliations in a publication separated by a semicolon

    Returns
    -------
    str
        SALT partner institutions separated by '|'.
    """
    salt_partners = set()
    for k, affiliation in enumerate(affiliations.split('; ')):
        # add SALT partner institutions
        if any(partner in affiliation for partner in config.SALT_PARTNERS):
            salt_partners.add(affiliation)

    return salt_partners


def get_saao_authors(affiliations, authors):
    """Return string of authors affiliated South African institutions.

    Params
    ------
    affiliations : list of affiliations in a publication separated by a semicolon

    Returns
    -------
    str
        authors affiliated South African institutions separated by '|'.
    """
    saao_authors = set()
    for k, affiliation in enumerate(affiliations.split('; ')):
        # only authors within the SAOO would have SALT as an affiliation
        saao_ins = ["SAAO", "South African Astronomical Observatory"]
        if any(institution in affiliation for institution in saao_ins):
            saao_authors.add(authors[k])
    return saao_authors


def count_authors_affiliated_to_sa_ins(affiliations, authors):
    """Return counts of authors affiliated South African institutions.

    Params
    ------
    affiliations : list of affiliations in a publication separated by a semicolon
    authors : list of authors in a publication

    Returns
    -------
    int
        counts of authors affiliated South African institutions
    """
    authors_aff_to_sa_inst = set()
    for affiliation in affiliations:
        for k, ins in enumerate(affiliation.split('; ')):
            if "South Africa" in affiliation:
                authors_aff_to_sa_inst.add(authors[k])

    return len(authors_aff_to_sa_inst)


def modify_list_contents(publication):
    # make some content more amenable to humans and xslxwriter alike
    list_value_columns = ['title', 'doi', 'fulltext_keywords', 'keyword', 'page']
    for c in list_value_columns:
        if c in publication and publication[c]:
            publication[c] = ', '.join(publication[c])


# By default, the start date is the current date, but you can pass a date on the command
# line instead.
if len(sys.argv) > 1:
    year, month, day = sys.argv[1].split("-")
    start_date = datetime.date(int(year), int(month), int(day))
    year, month, day = sys.argv[2].split("-")
    end_date = datetime.date(int(year), int(month), int(day))
else:
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=30)
queries = ADSQueries(from_date=start_date, to_date=end_date)

by_fulltext_keywords = queries.by_fulltext_keywords(config.KEYWORDS)
by_authors = queries.by_authors(config.AUTHORS.keys())
by_affiliations = queries.by_affiliations(config.AFFILIATIONS)
by_institutions = queries.by_affiliations(config.INSTITUTIONS)

all_queries = {**by_fulltext_keywords, **by_authors, **by_affiliations, **by_institutions}

# make sure the keywords are present
for b in by_fulltext_keywords:
    all_queries[b]['fulltext_keywords'] = by_fulltext_keywords[b]['fulltext_keywords']

# now that we have collected everything, we can flatten our map to a list
publications = [all_queries[b] for b in all_queries.keys()]
publications.sort(key=lambda p: p['bibcode'])

# exclude arXiv preprints
publications = [p for p in publications if 'arXiv' not in p['bibcode']]

# exclude certain journals
excluded_journals = [journal.lower() for journal in config.EXCLUDED_JOURNALS]
publications = [p for p in publications if p["pub"].lower() not in excluded_journals]

wos_queries = WoSQueries()
try:
    for i, p in enumerate(publications):
        # add refereed status
        p['refereed'] = p['property'] and 'REFEREED' in p['property']

        # add ADS url
        p['ads_url'] = 'https://ui.adsabs.harvard.edu/#abs/{0}/abstract'.format(p['bibcode'])

        print(f'Querying authors and affiliations for publication {i + 1} of {len(publications)}')
        authors, affiliations = get_authors_and_affiliations(p)

        # No. of authors on paper affiliated to a SA institution
        p['no_of_authors_aff_to_SA_ins'] = count_authors_affiliated_to_sa_ins(affiliations, authors)

        # First author institution and SALT partner institutions
        p['institute_of_first_author'] = affiliations[0]

        saao_authors = set()
        south_african_affiliations = set()
        salt_partners = set()
        for j, affiliation in enumerate(affiliations):

            if len(get_south_african_affiliations(affiliation)) > 0:
                for aff in get_south_african_affiliations(affiliation):
                    south_african_affiliations.add(aff)
            if len(get_saao_authors(affiliation, authors)) > 0:
                for author in get_saao_authors(affiliation, authors):
                    saao_authors.add(author)
            if len(get_salt_partners(affiliation)) > 0:
                for partner in get_salt_partners(affiliation):
                    salt_partners.add(partner)

        # removes all empty elements from the list
        p['authors_affiliated_with_SAAO'] = '; '.join(saao_authors)

        p['SA_institutions'] = '; '.join(south_african_affiliations)

        p['SALT_partners'] = '; '.join(salt_partners)

        print(f'Querying WoS for publication {i + 1} of {len(publications)}')
        check_doi_indexed_in_wos(p)
        # avoid HTTP 429 Too Many Requests errors
        time.sleep(1)

        modify_list_contents(p)

    print(f'Sending email to librarians...')
    columns = spreadsheet_columns()
    send_mails([
        dict(name='all.xlsx', content=publications_spreadsheet(publications, columns.keys()))
    ], columns)
except requests.exceptions.HTTPError as err:
    # print(err)
    raise
