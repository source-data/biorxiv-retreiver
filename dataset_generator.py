from biorxiv_retriever import BiorxivRetriever
from datetime import date
import json
from urllib.error import URLError

BASE_URL = "https://api.biorxiv.org/details/"

class DatasetGenerator:
    """
    Generates a dataset using the biorxiv API and its service details.
    It can get the data from medrxiv, biorxiv or both separately.
    By default, it will use only biorxiv and generate all the available data since 2011.
    """
    def __init__(self, server: str = "biorxiv", columns: list = ['abstract', 'category'],
                 start_date: str = '2011-01-01', end_date: str = str(date.today())):
        self.cursor = 0
        self.service = "details"
        self.server = server
        self.columns = columns
        self.start_date = start_date
        self.end_date = end_date
        self.url = f"{BASE_URL}{server}/{start_date}/{end_date}/{str(self.cursor)}/json"
        self.data_retriever = BiorxivRetriever("details", server, start_date=start_date,
                                               end_date=end_date, format_="json", cursor=str(self.cursor))

    def __call__(self):
        # TODO: Avoid the repeated papers or papers with multiple versions
        dataset = []
        while self.data_retriever.count == 100:
            url = f"{BASE_URL}{self.server}/{self.start_date}/{self.end_date}/{self.cursor}/json"
            try:
                self.data_retriever = BiorxivRetriever(self.service, self.server, start_date=self.start_date,
                                                       end_date=self.end_date, format_="json",
                                                       cursor=str(self.cursor))
            except URLError:
                self.data_retriever = BiorxivRetriever(self.service, self.server, start_date=self.start_date,
                                                       end_date=self.end_date, format_="json",
                                                       cursor=str(self.cursor))

            for paper in self.data_retriever.papers:
                for column in self.columns:
                    dataset.append(paper)

            self.cursor += 100
            break

        print("This is the call function")
        print(self.data_retriever.total_articles)
        return dataset

    def __str__(self):
        return f"""
        ============================================================
        Results from the medatadata retrieval of {self.server}.

        Total articles found {self.data_retriever.total_articles}
        URL generated {self.url}
        
        Data columns to generate dataset -> {self.columns}

        Search attributes: 
            server -> {self.server}
            service -> {self.service}
            start date -> {self.start_date}
            end date -> {self.end_date}

        Example of the first paper retrieved:
            {json.dumps(self.data_retriever.papers[0], indent=4, sort_keys=True)} 
        ============================================================
        """
