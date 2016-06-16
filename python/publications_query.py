import datetime
import json
import os
import subprocess

import config
from ads_queries import ADSQueries
from pdf_access import fetch_pdf


def ignore_tmp_bibcodes(bibcodes):
    """Filter out bibcodes which are temporary.

    Params:
    -------
    bibcodes: list of str
        Bibcodes to filter.

    Returns:
    --------
    list of str
        List of bibcodes lswithout the temporary ones.
    """

    return [bibcode for bibcode in bibcodes if 'tmp' not in bibcode]


def pdf_keywords_query(queries):
    """Query the publication PDFs for keywords.

    ADS is queried for the articles published in the list of journals defined in the configuration. The PDFs for these
    articles are downloaded and queried for rthe list of keywords defined in the configuration.

    Articles with a temporary bibcode are ignored.

    A tuple is returned. The first item in this tuple is a dictionary of the bibcodes for which at least one keyword
    was found and the keywords found. The second item is the list of bibcodes for which the keyword search couldn't
    be performed, for example because the PDF couldn't be downloaded.

    Params:
    -------
    queries: ADSQueries
        ADSQueries instance.

    Returns:
    --------
    tuple
        Tuple of a dictionary of bibcodes and keywords found and the list of bibcodes for which the keyword search
        couldn't be executed.

    """

    # get the bibcodes for the journals whose articles should be downloaded as pdf
    bibcodes = queries.by_journals(config.JOURNALS)

    # ignore temporary bibcodes
    bibcodes = ignore_tmp_bibcodes(bibcodes)

    # attempt to download all the pdfs
    for index, bibcode in enumerate(bibcodes):
        print('[{index}/{total}] Trying to get PDF for {bibcode}...'.format(index=index + 1, total=len(bibcodes), bibcode=bibcode))
        try:
            fetch_pdf(bibcode=bibcode, output_dir=config.OUTPUT_DIR)
        except BaseException as e:
            print('FAILED: {0}'.format(e))

    # get the keyword search parameters
    bibcodes.append('RXT6785')
    pdf_bibcodes = {os.path.join(config.OUTPUT_DIR, '{bibcode}.pdf'.format(bibcode=bibcode)):bibcode
                    for bibcode in bibcodes}
    pdfs = list(pdf_bibcodes.keys())
    params = json.dumps(dict(pdfs=pdfs, keywords=config.KEYWORDS))

    # perform the keyword search
    jar = os.path.join(os.path.dirname(__file__),
                       os.pardir,
                       'java',
                       'target',
                       'pdf-keyword-search-current.jar')
    p = subprocess.run(['java', '-jar', jar], input=bytearray(params, encoding='UTF-8'), stdout=subprocess.PIPE)
    results = json.loads(p.stdout.decode('UTF-8'))['results']

    # parse the results
    keywords_found = {pdf_bibcodes[r['pdf']]:r['keywords'] for r in results if r['keywords']}
    inconclusive = [pdf_bibcodes[r['pdf']] for r in results if r['keywords'] is None]

    return keywords_found, inconclusive


queries = ADSQueries(from_date=datetime.datetime.now().date(), to_date=datetime.datetime.now().date())

pdf_keywords_query(queries)