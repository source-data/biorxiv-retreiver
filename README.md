# biorxiv-retreiver

**biorxiv-retriever** is a resilient wrapper to the [Biorxiv API](https://api.biorxiv.org/). It
consists of two main classes: [DatasetGenerator](https://github.com/source-data/biorxiv-retreiver/blob/7b96ea7a03c3c445d68faf9e73983930b6022f9a/src/dataset_generator.py) 
and [BiorxivRetriever](https://github.com/source-data/biorxiv-retreiver/blob/7b96ea7a03c3c445d68faf9e73983930b6022f9a/src/biorxiv_retriever.py).
The former uses resilient HTTP requests to generate a dataset with the available preprints 
in [Biorxiv](https://biorxiv.org/). BiorxivRetriever is an API wrapper that allows for API
calls to any of the services supported by the Biorxiv API.

## Installing biorxiv-retriever

Clone the repository and setup a Python virtual environment:
```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt 
``` 

### Using biotxiv-retriever from the CLI

From the directory root you can get CLI help on how to call the commands using:

```bash
# To use BiorxivRetriever
python -m src.cli.search.search --help
# To use DatasetGenerator
python -m src.cli.create_data.create_data --help
```

#### Examples on using BiorxivRetriever
Using the details service of the [Biorxiv API](https://api.biorxiv.org/) to find all papers 
between first of May 2022 and the current date.
```bash
python -m src.cli.search.search details biorxiv \
        --start_date=2022-05-01
```
Using the details service of the [Biorxiv API](https://api.biorxiv.org/) to find all papers 
between first of May 2022 and the current date.
```bash
python -m src.cli.search.search details biorxiv \
        --start_date=2022-05-01
```

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

### Using biotxiv-retriever as a python module

