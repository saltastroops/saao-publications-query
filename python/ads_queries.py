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
        self.max_retries = 5

    def _by_journal(self, journal):
        retries = 0
        while retries <= self.max_retries:
            try:
                q = 'bibstem:{journal} AND pubdate:{pubdate}'.format(journal=journal, pubdate=self.pubdate)
                query = ads.SearchQuery(q=q, fl=['bibcode'], max_pages=self.max_pages)
                return [a.bibcode for a in list(query)]
            except ads.exceptions.APIResponseError:
                retries += 1
                print("Retrying...")
                if retries > self.max_retries:
                    raise


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
            bibcodes.extend(self._by_journal(journal))
        return bibcodes

    def _by_fulltext_keyword(self, keyword, publications):
        retries = 0
        while retries <= self.max_retries:
            try:
                q = 'full:"{keyword}" AND pubdate:{pubdate}'.format(keyword=keyword, pubdate=self.pubdate)
                query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
                for result in list(query):
                    if result.bibcode not in publications:
                        publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}
                        publications[result.bibcode]['fulltext_keywords'] = []
                    publications[result.bibcode]['fulltext_keywords'].append(keyword)
                return
            except ads.exceptions.APIResponseError:
                retries += 1
                print("Retrying...")
                if retries > self.max_retries:
                    raise


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
            self._by_fulltext_keyword(keyword, publications)

        return publications

    def _by_author(self, author, publications):
        retries = 0
        while retries <= self.max_retries:
            try:
                q = 'author:"{author}" AND pubdate:{pubdate}'.format(author=author, pubdate=self.pubdate)
                query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
                for result in list(query):
                    if result.bibcode not in publications:
                        publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}
                return
            except ads.exceptions.APIResponseError:
                retries += 1
                print("Retrying...")
                if retries > self.max_retries:
                    raise

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
            self._by_author(author, publications)

        return publications

    def _by_affiliation(self, affiliation, publications):
        retries = 0
        while retries <= self.max_retries:
            try:
                q = 'aff:"{affiliation}" AND pubdate:{pubdate}'.format(affiliation=affiliation, pubdate=self.pubdate)
                query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
                for result in list(query):
                    if result.bibcode not in publications:
                        publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}
                return
            except ads.exceptions.APIResponseError:
                retries += 1
                print("Retrying...")
                if retries > self.max_retries:
                    raise

    def by_affiliations(self, affiliations):
        """Query ADS for the publications with any of a list of affiliations.

        Each affiliation must be in the list of affiliations used by the ADS
        (https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv),
        and its name must be given exactly as in that list.

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
            self._by_affiliation(affiliation, publications)

        return publications

    def _by_institution(self, institution, publications):
        retries = 0
        while retries <= self.max_retries:
            try:
                q = 'institution:"{institution}" AND pubdate:{pubdate}'.format(
                    institution=institution, pubdate=self.pubdate
                )
                query = ads.SearchQuery(q=q, fl=self.fields, fq='database:astronomy', max_pages=self.max_pages)
                for result in list(query):
                    if result.bibcode not in publications:
                        publications[result.bibcode] = {f: getattr(result, f) for f in self.fields}
                return
            except ads.exceptions.APIResponseError:
                retries += 1
                print("Retrying...")
                if retries > self.max_retries:
                    raise

    def by_institutions(self, institutions):
        """Query ADS for the publications with any of a list of institutions.

        Each institution must be in the list of affiliations used by the ADS
        (https://github.com/adsabs/CanonicalAffiliations/blob/master/parent_child.tsv),
        and its name must be given exactly as in that list.

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
            self._by_institution(institution, publications)
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
            retries = 0
            while retries <= self.max_retries:
                try:
                    query = ads.SearchQuery(bibcode=bibcode, fl=self.fields, max_pages=self.max_pages)
                    details = list(query)[0]
                    return {f: getattr(details, f) for f in self.fields}
                except ads.exceptions.APIResponseError:
                    retries += 1
                    print("Retrying...")
                    if retries > self.max_retries:
                        raise
        except:
            details = {f: '' for f in self.fields}
            details['bibcode'] = bibcode
            return details
