import datetime
import os

import ads

import config


class ADSQueries:
    """Queries for the Astrophysics Data System (ADS).

    Publications with a temporary bibcode are ignored for all queries.

    Params:
    -------
    from_date: datetime.date
        Earliest date for which publications should be queried. Only the year and month are relevant.
    to_date: datetime.date
        Latest date for which publications should be queried. Only the year and month are relevant.
    """

    def __init__(self, from_date, to_date):
        ads.config.token = config.ADS_API_KEY
        self.pubdate = '[{from_date} TO {to_date}]'.format(from_date=from_date.strftime('%Y-%m'),
                                                           to_date=to_date.strftime('%Y-%m'))
        self.fields = [
            'abstract',
            'author',
            'bibcode',
            'doi',
            'page',
            'property',
            'pubdate',
            'volume'
        ]
        self.num_pages = 30

    def by_journals(self, journals):
        """Query ADS for the publications published in any of a list of journals.

        Contrary to the other query methods in this class a list of bibcodes is returned.

        Params:
        -------
        journals: list of str
            The list of journals to query. The abbreviation used in ADS bibcodes must be used for the journals. For
            example, Monthly Notices and Astronomy & Astrophysics woulds be specified as 'MNRAS' and 'A&A'.

        Returns:
        --------
        list of str
            The bibcodes of publications published in any of the journals.
        """

        bibcodes = []
        for journal in journals:
            q = 'bibstem:{journal} AND pubdate:{pubdate}'.format(journal=journal, pubdate=self.pubdate)
            query = ads.SearchQuery(q=q, fl=['bibcode'])
            bibcodes.extend([a.bibcode for a in list(query)])
        return bibcodes

    def by_keywords(self, keywords):
        """Query ADS for the publications containing any of a list of keywords.

        Aliases of the keywords (as determined by ADS) are included in the search.

        Params:
        -------
        keywords: list of str
            The list of keywords to search for.

        Returns:
        --------
        list of Publication
            The publications containing any of the keywords (or their synonyms).
        """

        publications = dict()
        for keyword in keywords:
            print('Searching for ' + keyword)
            q = 'full:"{keyword}" AND pubdate:{pubdate}'.format(keyword=keyword, pubdate=self.pubdate)
            query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy')
            for result in list(query):
                if result.bibcode not in publications:
                    publications[result.bibcode] = {f:getattr(result, f) for f in self.fields}
                    publications[result.bibcode]['keywords'] = []
                publications[result.bibcode]['keywords'].append(keyword)

        return publications

    def by_authors(self, authors):
        """Query ADS for the publications containing any of a list of authors.

        The authors should be specified in the form last_name, first_name other_initials (such as 'Potter, Stephen' or
        'Potter, Stephen B'). See http://adsabs.github.io/help/search/search-syntax for more details.

        Params:
        -------
        authors: list of str
             The list of authors to search for.

        Returns:
        --------
        list of Publication
            The publications containing any of the authors.
        """

        pass

    def by_affiliations(self, affiliations):
        """Query ADS for the publications with any of a list of affiliations.

        It is sufficient to give a substring of the affiliation; for example publications with 'South African
        Astronomical Observatory' are found if 'South African Astronomical' is specified as affiliation.

        Params:
        -------
        affiliations: list of str
            The affiliations to search for.

        Returns:
        --------
        list of Publication
            The publications with any of the affiliations.
        """
        pass

    def full_details(self, bibcode):
        """Query ADS for the full details of a publication.

        The full details are the list of fields defined in self.fields. They are returned as a dictionary. If the query
        fails, empty strings are returned for all the fields (with the exception of the bibcode).

        Params:
        -------
        bibcode: str
            The bibcode.

        Returns:
        --------
        dict
            The full details.
        """

        try:
            query = ads.SearchQuery(bibcode=bibcode, fl=self.fields)
            details = list(query)[0]
            return {f:getattr(details, f) for f in self.fields}
        except:
            details = {f:'' for f in self.fields}
            details['bibcode'] = bibcode
            return details

