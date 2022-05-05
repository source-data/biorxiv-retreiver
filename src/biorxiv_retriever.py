import json
from urllib import request
from datetime import datetime

BASE_URLs = {"details": "https://api.biorxiv.org/details/",
             "pubs": "https://api.biorxiv.org/pubs/",
             "pub": "https://api.biorxiv.org/pub/",
             "publisher": "https://api.biorxiv.org/publisher/",
             "sum": "https://api.biorxiv.org/sum/",
             "usage": "https://api.biorxiv.org/usage/"}


class BiorxivRetriever:
    """
    Wrapper that retrieves data from the Biorxiv and Medrxiv APIs.
    Documentation and implementation based on: https://api.biorxiv.org/
    Attributes
    ----------
    service : str
        API service to be used to retrieve the data. To choose between:
        ['details', 'pubs','pub','publisher','sum','usage'].
        * 'details' - Where metadata for multiple papers is returned with results are paginated with 100 papers
                        served in a call. The 'cursor' value can be used to iterate through the result. Attributes
                        to be used ['server', 'start_date', 'end_date', 'cursor', 'format'] or
                        ['server', 'doi', 'format']. The former will return a series of articles while the latter
                        will return only the article matching the doi attribute.
        * 'pub' - Only for biorxiv, it returns metadata of the published article details.
                    Attributes to be used ['interval', 'cursor', 'format'].
        * 'pubs' - metadata for preprint published article detail for specified server (bioRxiv or medRxiv)
                        for multiple papers is returned with results are paginated with 100 papers
                        served in a call. The 'cursor' value can be used to iterate through the result. Attributes
                        to be used ['server', 'start_date', 'end_date', 'cursor', 'format'] or
                        ['server', 'doi', 'format']. The former will return a series of articles while the latter
                        will return only the article matching the doi attribute.
        * 'publisher' - returns metadata of the publisher of the articles. It uses the attributes
                        ['prefix', 'interval', 'cursor'].
        * 'sum' - Returns summary statistics of the content. It uses the attributes
                        ['interval', 'format'].
        * 'usage' - Returns summary statistics of the usage. It uses the attributes
                        ['interval', 'format'].
    server : str
        Server to look for the preprints. 'biorxiv' or 'medrxiv'.
    interval : str, optional
        **For service='sum' and service='usage'** interval takes 'm' monthly and 'y' yearly as values.
    cursor : int, optional
        Will be used to iterate on the result.
    doi : int,
        DOI identifier of a given article.
    format_ : str, optional
        The two available formats are json and xml. Defaults to json. **For service='sum' and service='usage'**
        format can also be set to 'csv' to generate a .csv file.
    prefix : str, optional
         String of the publisher prefix, eg '10.15252'

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self, service: str, server: str, start_date: str = '2020-01-01',
                 end_date: str = '2022-03-31', interval: str = 'm', cursor: str = 0,
                 format_: str = 'json', prefix: str = '10.15252', doi: str = ""):
        """
        Parameters
        ----------
    service : str
        API service to be used to retrieve the data. To choose between:
        ['details', 'pubs','pub','publisher','sum','usage'].
    server : str
        Server to look for the preprints. 'biorxiv' or 'medrxiv'.
    start_date : str
        YYYY-MM-DD format. Must be prior to end_date
    end_date : str
        YYYY-MM-DD format
    interval : str, optional
        **For service='sum' and service='usage'** interval takes 'm' monthly and 'y' yearly as values.
    cursor : int, optional
        Will be used to iterate on the result.
    doi : int, optional
        DOI identifier of a given article.
    format_  : str, optional
        The two available formats are json and xml. Defaults to json. **For service='sum' and service='usage'**
        format can also be set to 'csv' to generate a .csv file.
    prefix : str, optional
         String of the publisher prefix, eg '10.15252'
        """
        assert service in BASE_URLs.keys(), \
            f"Please ensure that you are defining service as one of the following values: {BASE_URLs.keys()}"
        self.base_url = BASE_URLs[service]
        self.start_date = start_date
        self.end_date = end_date
        self.server = server
        self.service = service
        self.doi = doi
        self.format = format_
        self.interval = interval
        self.cursor = cursor
        self.prefix = prefix

        if service in ['details', 'pubs']:
            if doi:
                self.url = f"{self.base_url}{server}/{doi}/na/{format_}"
                self.start_date = "NOT APPLICABLE"
                self.end_date = "NOT APPLICABLE"
                self.interval = "NOT APPLICABLE"
                self.cursor = "NOT APPLICABLE"
                self.prefix = "NOT APPLICABLE"
            else:
                assert self._date_assertion(), "start_date must be prior to end_date"
                self.url = f"{self.base_url}{server}/{start_date}/{end_date}/{cursor}/{format_}"
                self.doi = "NOT APPLICABLE"
                self.interval = "NOT APPLICABLE"
                self.prefix = "NOT APPLICABLE"
        elif service == 'pub':
            self.url = f"{self.base_url}{start_date}/{end_date}/{cursor}"
            self.interval = "NOT APPLICABLE"
            self.doi = "NOT APPLICABLE"
            self.prefix = "NOT APPLICABLE"
            self.server = "NOT APPLICABLE"
            self.format_ = "NOT APPLICABLE"
        elif service == 'publisher':
            self.url = f"{self.base_url}{prefix}/{start_date}/{end_date}/{cursor}"
            self.interval = "NOT APPLICABLE"
            self.doi = "NOT APPLICABLE"
            self.server = "NOT APPLICABLE"
            self.format = "NOT APPLICABLE"
        elif service in ['sum', 'usage']:
            self.url = f"{self.base_url}{interval}/{format_}"
            self.start_date = "NOT APPLICABLE"
            self.end_date = "NOT APPLICABLE"
            self.doi = "NOT APPLICABLE"
            self.server = "NOT APPLICABLE"
            self.cursor = "NOT APPLICABLE"
            self.prefix = "NOT APPLICABLE"
        else:
            raise ValueError(f"Please define service as one of the following values: {BASE_URLs.keys()}")

        self.messages = self._retrieve_metadata()['messages']
        if self.service not in ["sum", "usage"]:
            self.papers = self._retrieve_metadata()['collection']
            self.total_articles = self.messages = self._retrieve_metadata()['messages'][0]['total']
            self.count = self.messages = self._retrieve_metadata()['messages'][0]['count']
        else:
            self.papers = self._retrieve_metadata()['bioRxiv content statistics']
            self.total_articles = None

    def _retrieve_metadata(self):
        """Returns the metadata from the Biorxiv API.
        :returns dict with the API response. The API will have 'messages' and 'collections' as keys.
                'messages' contains information of the http request. 'collections' is a `list`
                containing the metadata, stored as `dict` objects."""
        response = json.loads(request.urlopen(self.url).read().decode("utf-8"))
        if self.service in ["sum", "usage"]:
            assert response['messages'][
                       'status'] == "ok", f"⚠️ URL is not correct. Do you have the correct interval 'm' or 'y'?"
        else:
            assert response['messages'][0][
                       'status'] == 'ok', f"⚠️ Do you use the correct server biorxiv or medrxiv? {response['messages'][0]['status']} ⚠️, \n{self.url}"
        return response

    def _date_assertion(self):
        start = datetime.strptime(self.start_date, '%Y-%m-%d')
        end = datetime.strptime(self.end_date, '%Y-%m-%d')
        return start < end

    def __str__(self):
        return f"""
        ============================================================
        Results from the medatadata retrieval of {self.server}.

        Total articles found {self.total_articles}
        URL generated {self.url}

        Search attributes: 
            server -> {self.server}
            service -> {self.service}
            doi -> {self.doi}
            start date -> {self.start_date}
            end date -> {self.end_date}
            format -> {self.format}
            interval -> {self.interval}
            cursor -> {self.cursor}
            interval -> {self.prefix}

        Example of the first paper retrieved:
            {json.dumps(self.papers[0], indent=4, sort_keys=True)} 
        ============================================================
        """
