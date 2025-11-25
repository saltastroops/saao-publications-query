from enum import Enum

import requests

import config


class WoSIndexedStatus(Enum):
    INDEXED = "Indexed"
    NOT_INDEXED = "Not indexed"
    UNKNOWN = "Unknown"

class WoSQueries:
    BASE_URL = 'https://wos-api.clarivate.com/api/woslite'

    def __init__(self):
        wos_api_key = config.WOS_API_KEY
        self.session = requests.Session()
        self.session.headers.update({'X-ApiKey': wos_api_key})

    def is_doi_indexed(self, doi):
        """
        Check whether a DOI is indexed on the Web of Science.

        Params
        ------
        doi : str
            Document object identifier (DOI).

        Returns
        -------
        WosIndexedStatus
             Whether the DOI is indexed.

        """

        # If there is no DOI, it cannot be indexed.
        if not doi:
            return WoSIndexedStatus.NOT_INDEXED

        # Query the WoS for the DOI.
        params = {
            'databaseId': 'WOS',
            'usrQuery': f'do={doi}',
            'firstRecord': 1,
            'count': 1
        }
        res = self.session.get(WoSQueries.BASE_URL, params=params)

        # If the query fails, we don't know whether the DOI is indexed.
        if res.status_code != 200:
            return WoSIndexedStatus.UNKNOWN

        # Check whether a publication was found for the DOI.
        search_results = res.json()
        publications_data = search_results['Data']
        if len(publications_data) == 0:
            return WoSIndexedStatus.NOT_INDEXED

        # Sanity check: Does the search result have the correct DOI?
        if publications_data[0]['Other']['Identifier.Doi']:
            return WoSIndexedStatus.INDEXED
        else:
            return WoSIndexedStatus.UNKNOWN


if __name__ == '__main__':
    wos = WoSQueries()
    print(wos.is_doi_indexed('10.1051/0004-6361/201834039'))

