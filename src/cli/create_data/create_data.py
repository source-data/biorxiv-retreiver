from ...dataset_generator import DatasetGenerator
import argparse
from datetime import date

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieves bioRxiv preprint results and generates a dataset file",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('server', nargs="?", default="biorxiv", help="""Server to retrieve data from. 'biorxiv' or 
                                                                        'medrxiv'. To be use for the services
                                                                        ['details', 'pubs']""")
    parser.add_argument('--start_date', default='2011-01-01', help="Start date for the search (format YYYY-MM-DD)")
    parser.add_argument('--end_date', default=str(date.today()), help="End date for the search (format YYYY-MM-DD)")
    parser.add_argument('--save_folder', nargs="?", default="../data", help="""Name API fields to retrieve. Comma separated.
                                                                    Only valid for 'task'='create_dataset'.""")
    parser.add_argument('--email', nargs="?", default="",
                        help="""Email for identification. It is advisable but not mandatory.""")
    parser.add_argument('--filename', nargs="?", default="biorxiv-dataset.json",
                        help="""Name of the file with the data output.""")
    parser.add_argument('--xml', nargs="?", default="False",
                        help="""If True, it will add the XML files containing the full text of the articles to the dataset.""")

    args = parser.parse_args()
    server = args.server
    start_date = args.start_date
    end_date = args.end_date
    save_folder = args.save_folder
    email = args.email
    xml = args.xml
    filename = args.filename

    output = DatasetGenerator(server=server, start_date=start_date, end_date=end_date,
                              save_folder=save_folder, email=email, xml=xml, filename=filename)

    output()
