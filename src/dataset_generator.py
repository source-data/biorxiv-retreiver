from src.biorxiv_retriever import BiorxivRetriever
from datetime import date
import json
from urllib.error import URLError
from os.path import join
import os
from os import path

BASE_URL = "https://api.biorxiv.org/details/"


class DatasetGenerator:
    """
    Generates a dataset using the biorxiv API and its service details.
    It can get the data from medrxiv, biorxiv or both separately.
    By default, it will use only biorxiv and generate all the available data since 2011.

    It stores the data in a json file that can be further processed to obtained the desired data
    """
    def __init__(self, server: str = "biorxiv", columns: list = ['abstract', 'category'],
                 start_date: str = '2011-01-01', end_date: str = str(date.today()),
                 save_folder: str = "./data", filename: str = "biorxiv_data_generator.json"):
        """
        Parameters
        ----------
        server : str
            Server to look for the preprints. 'biorxiv' or 'medrxiv'.
        start_date : str, optional
            YYYY-MM-DD format. Must be prior to end_date. Defaults to '2011-01-01' to get all existing biorxiv data.
        end_date : str, optional
            YYYY-MM-DD format. Defaults to `date.today()`
        save_folder : str, optional
            Folder to write the output data.
        filename : str, optional
            Name of file containing the json output.
        """
        self.cursor = 0
        self.service = "details"
        self.server = server
        self.columns = columns
        self.start_date = start_date
        self.end_date = end_date
        self.url = f"{BASE_URL}{server}/{start_date}/{end_date}/{str(self.cursor)}/json"
        self.save_folder = save_folder
        self.filename = filename
        self.data_retriever = BiorxivRetriever("details", server, start_date=start_date,
                                               end_date=end_date, format_="json", cursor=str(self.cursor))

    def __call__(self) -> dict:
        """Will call the Biorxiv API as many times as necessary to generate a json file with the
        metadata of all the papers found by the search parameters.
        It writes the data as a `json` object to the specified `self.save_folder` at class instantiation.
        :returns `dict`
        """
        dataset = {}
        while self.data_retriever.count == 100:
            print(f"""Calling entry number {self.cursor} from a total of {self.data_retriever.total_articles}. Progress of {round(100*self.cursor/self.data_retriever.total_articles, 2)}%""", end='\r')

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
                dataset = self._remove_duplicates(dataset, paper)

            self.cursor += 100

        self._write_file(dataset)

        return dataset

    @staticmethod
    def _remove_duplicates(history: dict, new: dict) -> dict:
        """
        Given a dictionary with a history of papers and a new paper to be added to history,
        it will add the paper. In case the paper already exists, it will overwrite it in case
        the version is older than the version in history.
        """
        if new["doi"] not in list(history.keys()):
            history[new["doi"]] = new
        else:
            if int(new["version"]) > int(history[new["doi"]]["version"]):
                history[new["doi"]] = new
            else:
                pass
        return history

    def _write_file(self, data: dict) -> None:
        """Writes data into a json file in the self.data_folder provided at class instantiation."""
        if not path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        with open(join(self.save_folder, self.filename), "w") as fp:
            json.dump(data, fp)

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
