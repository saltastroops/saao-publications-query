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

    def __init__(self, from_date, to_date, max_pages=30):
        ads.config.token = config.ADS_API_KEY
        self.pubdate = '[{from_date} TO {to_date}]'.format(from_date=from_date.strftime('%Y-%m'),
                                                           to_date=to_date.strftime('%Y-%m'))
        self.fields = [
            'abstract',
            'aff',
            'author',
            'bibcode',
            'data',
            'doi',
            'keyword',
            'page',
            'property',
            'pub',
            'pubdate',
            'title',
            'volume'
        ]
        self.max_pages = max_pages

    def by_journals(self, journals):
        """Query ADS for the publications published in any of a list of journals.

        Contrary to the other query methods in this class a list of bibcodes is returned, as otherwise tons of
        essentially useless data would be requested (given that only a tiny minority of articles will be relevant).

        Params:
        -------
        journals: list of str
            The list of journals to query. The abbreviation used in ADS bibcodes must be used for the journals. For
            example, Monthly Notices and Astronomy & Astrophysics would be specified as 'MNRAS' and 'A&A'.

        Returns:
        --------
        list of str
            The bibcodes of publications published in any of the journals.
        """

        bibcodes = []
        for journal in journals:
            q = 'bibstem:{journal} AND pubdate:{pubdate}'.format(journal=journal, pubdate=self.pubdate)
            query = ads.SearchQuery(q=q, fl=['bibcode'], max_pages=self.max_pages)
            bibcodes.extend([a.bibcode for a in list(query)])
        return bibcodes

    def by_fulltext_keywords(self, keywords):
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
            query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
            for result in list(query):
                if result.bibcode not in publications:
                    publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}
                    publications[result.bibcode]['fulltext_keywords'] = []
                publications[result.bibcode]['fulltext_keywords'].append(keyword)

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

        publications = dict()
        for author in authors:
            print('Searching for ' + author)
            q = 'author:"{author}" AND pubdate:{pubdate}'.format(author=author, pubdate=self.pubdate)
            query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
            for result in list(query):
                if result.bibcode not in publications:
                    publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}

        return publications

    def by_affiliations(self, affiliations):
        """Query ADS for the publications with any of a list of affiliations.

        It is sufficient to give a substring of the affiliation; for example publications with 'South African
        Astronomical Observatory' are found if 'South African Astronomical Observatory' is specified as affiliation.

        Params:
        -------
        affiliations: list of str
            The affiliations to search for.

        Returns:
        --------
        list of Publication
            The publications with any of the affiliations.
        """

        publications = dict()
        for affiliation in affiliations:
            print('Searching for ' + affiliation)
            q = 'aff:"{affiliation}" AND pubdate:{pubdate}'.format(affiliation=affiliation, pubdate=self.pubdate)
            query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
            for result in list(query):
                if result.bibcode not in publications:
                    publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}

        return publications

    def by_institutions(self, institutions):
        """Query ADS for the publications with any of a list of institutions.

        It is sufficient to give an abbreviation string of the institution/affiliation listed here
        https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv;

        for example institutions with 'SAAO' are found if
        'South African Astronomical Observatory/SAAO' is specified as an institution.

        NB: It is crucial to stick to the names given there.

        Params:
        -------
        institutions: list of str
            The institutions to search for.

        Returns:
        --------
        list of Publication
            The publications with any of the institutions.
        """

        publications = dict()
        for institution in institutions:
            print('Searching for ' + institution)
            q = 'institution:"{institution}" AND pubdate:{pubdate}'.format(
                institution=institution, pubdate=self.pubdate
            )
            query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
            for result in list(query):
                if result.bibcode not in publications:
                    publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}

        return publications

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
            query = ads.SearchQuery(bibcode=bibcode, fl=self.fields, max_pages=self.max_pages)
            details = list(query)[0]
            return {f: getattr(details, f) for f in self.fields}
        except:
            details = {f: '' for f in self.fields}
            details['bibcode'] = bibcode
            return details
