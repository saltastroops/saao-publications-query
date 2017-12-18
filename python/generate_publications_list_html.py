"""
Generate HTML containing the SAAO publications list. This can be used on the SAAO's website.

The publications are read from an Excel spreadsheet with the following columns:

PSAAO: Unique identifier for the publication.
Responsibility: List of authors.
TITLE: Publication title.
REF: Journal.
VOL: Journal volume.
FPG: First page of the publication.
URL: URL for this publication. In most cases this is a link to the ADS.

The generated HTML is printed to the standard output.

Usage: python generate_publications_list_html.py /path/to/spreadsheet
"""

import argparse
import datetime
import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('spreadsheet', help='spreadsheet with the SAAO publication data')
args = parser.parse_args()


def create_html():
    df = pd.read_excel(args.spreadsheet)

    start_year = 1971
    end_year = datetime.datetime.now().year

    html = ''
    for year in range(end_year, start_year - 1, -1):
        html += '<h2>{year}</h2>\n'.format(year=year)
        df_year = df[np.isclose(df['YEAR'].values, year)]
        for _, row in df_year.iterrows():
            html += create_row_content(year, row)

    return html


def create_row_content(year, row):
    id = row['PSAAO']
    authors = row['Responsibility']
    title = row['TITLE']
    ref = row['REF']
    volume = row['VOL']
    first_page = row['FPG']
    url = row['URL']
    telescopes = row['TELESCOPE']

    return '''<p><strong>{id}. </strong> {authors}, {year}. {title} {location} {link} {telescopes}</p>\n'''\
        .format(id=id,
                authors=create_authors(authors),
                title='{title}.'.format(title=title.strip()) if not pd.isna([title]) else '',
                year=year,
                location=create_location(ref, volume, first_page),
                link=create_link(url),
                telescopes=create_telescopes(telescopes))


def create_authors(authors):
    if pd.isna([authors]):
        return ''
    authors = authors.strip(', ')\
        .replace('( &', '(&')\
        .replace('& ', '&amp; ')
    parenthesis = authors.find('(')
    if parenthesis != -1:
        return '{first}<em>{second}</em>'\
            .format(first=authors[:parenthesis], second=authors[parenthesis:])
    else:
        return authors


def create_location(ref, volume, first_page):
    location = ''
    if pd.isna([ref]):
        return location
    location += '<em>{ref}</em>'.format(ref=ref.strip().replace('& ', '&amp; '))
    if pd.isna([volume]):
        return location
    location += ', <strong>{volume}'.format(volume=volume)
    if pd.isna([first_page]):
        first_page = None
    if first_page and 'pp' in str(first_page).lower():
        first_page = None
    if first_page:
        location += ': '
    location += '</strong>'
    if first_page:
        location += str(first_page)
    location += '.'

    return location


def create_link(url):
    if url and not pd.isna([url]):
        title = 'ADS' if 'saaoads.' in url or 'adsabs.' in url else 'Link'
        return '<a href="{url}">{title}</a>'.format(url=url, title=title)
    else:
        return ''


def create_telescopes(telescopes):
    if pd.isna([telescopes]):
        return ''
    return '<em>[{telescopes}]</em>'.format(telescopes=telescopes.replace('|', ', '))


print(create_html())