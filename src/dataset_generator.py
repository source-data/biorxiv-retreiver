from datetime import date
import json
from os.path import join
import os
from os import path
from src.requester import BiorxivRequester
import requests

BASE_URL = "https://api.biorxiv.org/details/"


class BiorxivDataGenerator:
    """
    Generates a dataset using the biorxiv API and its service details.
    It can get the data from medrxiv, biorxiv or both separately.
    By default, it will use only biorxiv and generate all the available data since 2011.

    It stores the data in a json file that can be further processed to obtained the desired data
    CLI usage:
        ```bash
        python main.py details biorxiv create_dataset --start_date 2022-05-01
        ```
    Usage within a python module
        ```python
        datagen = DatasetGenerator()
        dataset = datagen()
        ```

    """
    def __init__(self, server: str = "biorxiv",
                 start_date: str = '2011-01-01', end_date: str = str(date.today()),
                 save_folder: str = "./data", filename: str = "biorxiv_data_generator.json", email: str = "",
                 xml: bool = False):
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
        email : str, optional
            Email for identification. It is advisable for polite requests but not mandatory.
        """
        self.cursor = 0
        self.count = 100
        self.service = "details"
        self.server = server
        self.start_date = start_date
        self.end_date = end_date
        self.url = f"{BASE_URL}{server}/{start_date}/{end_date}/{str(self.cursor)}/json"
        self.save_folder = save_folder
        self.filename = filename
        self.xml = xml
        if email:
            self.headers = {
                            "From": f"{email}",
                            "Accept": "application/json",
                            }
        else:
            self.headers = {"Accept": "application/json"}

    def __call__(self) -> dict:
        """Will call the Biorxiv API as many times as necessary to generate a json file with the
        metadata of all the papers found by the search parameters.
        It writes the data as a `json` object to the specified `self.save_folder` at class instantiation.
        :returns `dict`
        """
        dataset = {}
        while self.count == 100:
            self.url = f"{BASE_URL}{self.server}/{self.start_date}/{self.end_date}/{self.cursor}/json"
            self.data_retriever = BiorxivRequester(self.url, self.headers)
            response = self.data_retriever()
            self.total_articles = response['messages'][0]['total']
            self.count = response['messages'][0]['count']
            print(f"""Calling entry number {self.cursor} from a total of {self.total_articles}. Progress of {round(100 * self.cursor / self.total_articles, 2)}%""", end='\r')
            for paper in response['collection']:
                dataset = self._remove_duplicates(dataset, paper)
                if self.xml:
                    self._dl_source_xml(paper)

            self.cursor += 100
        self.paper = paper
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

    def _dl_source_xml(self, paper: dict) -> None:
        """Writes data into a json file in the self.data_folder provided at class instantiation."""
        xml_folder = join(self.save_folder, "xml")
        if not path.exists(xml_folder):
            os.makedirs(xml_folder)

        source_url = paper.get("jatsxml", None)
        if source_url:
            r = requests.get(source_url, allow_redirects=True)
            open(f"{join(xml_folder, paper['doi'])}.xml", 'wb').write(r.content)

    def __str__(self):
        return f"""
        ============================================================
        Results from the medatadata retrieval of {self.server}.

        Total articles found {self.total_articles}
        URL generated {self.url}

        Search attributes:
            server -> {self.server}
            service -> {self.service}
            start date -> {self.start_date}
            end date -> {self.end_date}

        Example of paper:
            {json.dumps(self.paper, sort_keys=True, indent=4)}
        ============================================================
        """
