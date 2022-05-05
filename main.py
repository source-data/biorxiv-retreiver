from src.biorxiv_retriever import BiorxivRetriever
from src.dataset_generator import DatasetGenerator
import argparse
from datetime import date

def main():
    """
    Check Thomas code in
    https://github.com/embo-press/traxiv/blob/master/src/biorxiv.py
    :return:
    """

    parser = argparse.ArgumentParser(description="Retrieves bioRxiv preprint for journal",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('service', nargs="?", default="pubs", help="""API service to be used to retrieve the data. 
                                                                        To choose between:['details', 'pubs','pub',
                                                                        'publisher','sum','usage'].
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
                        ['interval', 'format']""")

    parser.add_argument('server', nargs="?", default="biorxiv", help="""Server to retrieve data from. 'biorxiv' or 
                                                                        'medrxiv'. To be use for the services
                                                                        ['details', 'pubs']""")
    parser.add_argument('task', nargs="?", default="retrieve", help="""Retrieve gets the response of the API. create_dataset
                                                                        outputs a dataset
                                                                        the details service for any of both servers.
                                                                        ['retrieve', 'create_dataset']""")
    parser.add_argument('--start_date', default='2011-01-01', help="Start date for the search (format YYYY-MM-DD)")
    parser.add_argument('--end_date', default=str(date.today()), help="End date for the search (format YYYY-MM-DD)")
    parser.add_argument('--doi', nargs="?", default="", help="DOI identifier of a given article.")
    parser.add_argument('--prefix', nargs="?", default="10.15252", help="The prefix of the publisher.")
    parser.add_argument('--format', nargs="?", default="json", help="Format of returning data")
    parser.add_argument('--interval', nargs="?", default="y", help="""Can be (m)onthly or (y)early. Only to use with 
                                                                        ["sum", "usage"]. Note that usage seems to be
                                                                        working only with monthly.""")
    parser.add_argument('--cursor', nargs="?", default="0", help="""Will be used to iterate on the result if this
                                                                    contains more than 100 entries.""")
    parser.add_argument('--columns', nargs="?", default="abstract,category", help="""Name API fields to retrieve. Comma separated.
                                                                    Only valid for 'task'='create_dataset'.""")
    parser.add_argument('--save_folder', nargs="?", default="../data", help="""Name API fields to retrieve. Comma separated.
                                                                    Only valid for 'task'='create_dataset'.""")

    args = parser.parse_args()
    service = args.service
    server = args.server
    start_date = args.start_date
    end_date = args.end_date
    doi = args.doi
    prefix = args.prefix
    format_ = args.format
    interval = args.interval
    cursor = args.cursor
    task = args.task
    columns = args.columns.split(",")
    save_folder = args.save_folder

    if task == "retrieve":
        output = BiorxivRetriever(service, server, start_date=start_date, end_date=end_date,
                      format_=format_, cursor=cursor, doi=doi, prefix=prefix, interval=interval)
    if task == "create_dataset":
        # Do a while loop. Get always count and if count < 100 stop after that iteration.
        output = DatasetGenerator(server=server, columns=columns, start_date=start_date, end_date=end_date)

    print(output)
    print(output())
    return output


if __name__ == "__main__":
    main()
