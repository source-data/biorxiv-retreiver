from ...biorxiv_retriever import BiorxivRetriever
import argparse
from datetime import date

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Retrieves metadata of Biorxi API",
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
    parser.add_argument('--save_folder', nargs="?", default="../data", help="""Name API fields to retrieve. Comma separated.
                                                                    Only valid for 'task'='create_dataset'.""")
    parser.add_argument('--filename', nargs="?", default="biorxiv-metadata.json",
                        help="""Name of the file with the data output.""")

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
    save_folder = args.save_folder
    filename = args.filename

    output = BiorxivRetriever(service, server, start_date=start_date, end_date=end_date,
                  format_=format_, cursor=cursor, doi=doi, prefix=prefix, interval=interval,
                            save_folder=save_folder, filename=filename)

    output()
