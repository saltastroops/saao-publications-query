import io
import os

import ads
import PyPDF2
import requests

import config

def fetch_pdf(bibcode, output_dir):
    '''Fetch and save the pdf for an article.

    An attempt is made to download the publisher article from ADS. If this attempt fails, ADS is queried for the DOI.
    If the DOI has been assigned by Elsevier the Science Direct API is used to query for the article pdf.
    If the DOI has been assigned by Springer, a libk to trhe articl;e is constructyed and used to get the pdf.

    If the article could be downloaded and is a pdf the pdf is stored in the output directory, using <bibcode>/pdf as
    the file name. Otherwise an exception is raised.

    If the pdf for the bibcode exists in the output directory already, nothing is done.

    Params:
    -------
    bibcode: str
        ADS bibcode.
    output_dir: str
        Output directory.

    Returns:
    --------
    void
    '''

    # don't re-download an existing pdf
    pdf_path = os.path.join(output_dir, bibcode + '.pdf')
    if os.path.isfile(pdf_path):
        return

    # get the abstract page for the bibcode
    response = requests.get(
        url='http://adsabs.harvard.edu/cgi-bin/nph-data_query',
        params={
            'bibcode': bibcode,
            'link_type': 'ARTICLE',
            'db_key': 'AST',
            'high': '',
        },
    )
    if response.status_code == 404:
        # get the DOI of the publication
        q = 'bibcode:{bibcode}'.format(bibcode=bibcode)
        ads.config.token = config.ADS_API_KEY
        query = ads.SearchQuery(q=q, fl=['doi'])
        results = list(query)
        if not results or not results[0].doi:
            raise BaseException('No DOI found for bibcode: {bibcode}'.format(bibcode=bibcode))
        doi = results[0].doi[0]

        if doi.startswith('10.1016'):
            # the publisher is Elsevier
            # ask Science Direct for the pdf
            headers = {
                'Accept': 'application/pdf',
                'X-ELS-APIKey': config.SCIENCE_DIRECT_API_KEY
            }
            response = requests.get(
                url= 'http://api.elsevier.com/content/article/doi/{doi}'.format(doi=doi),
                headers=headers
            )
            if response.status_code != 200:
                raise BaseException('Science Direct API query failed with status code {code}'
                                    .format(code=response.status_code))
        elif doi.startswith('10.1007') or doi.startswith('10.1134'):
            # the publisher is Springer
            url = 'http://link.springer.com/content/pdf/{doi}'.format(doi=doi.replace('/', '%2F'))
            response = requests.get(url)
        else:
            raise BaseException('I do not know how to get the pdf for this DOI: {doi}'.format(doi=doi))

    elif response.status_code != 200:
        raise BaseException('HTTP request failed with status code {0}'.format(response.status_code))

    # make sure the downloaded file really is a pdf
    pdf = io.BytesIO(response.content)
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    pdf_reader.getPage(0)

    # it seems we have a pdf, so we might as well save it
    out = open(pdf_path, 'wb')
    out.write(response.content)
    out.close()
