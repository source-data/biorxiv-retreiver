# biorxiv-retreiver

**biorxiv-retriever** is a resilient wrapper to the [Biorxiv API](https://api.biorxiv.org/). It
consists of two main classes: [BiorxivDataGenerator](https://github.com/source-data/biorxiv-retreiver/blob/7b96ea7a03c3c445d68faf9e73983930b6022f9a/src/dataset_generator.py) 
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
Same as in the previous example with data from [Medrxiv](https://medrxiv.org/).
```bash
python -m src.cli.search.search details medrxiv \
        --start_date=2022-05-01
```
Search for details of article publishers. In this case, the publisher with a `prefix`
doi `10.15252`
```bash
python -m src.cli.search.search publisher biorxiv \
        --prefix=10.15252 \
        --start_date=2021-05-01
```
Show the summary of content statistics in Biorxiv
```bash
python -m src.cli.search.search sum biorxiv \
        --interval=m
```

#### Examples on using DatasetGenerator

Get all the available metadata in biorxiv since 4th May 2022 <(-_-)> may the force be with you.
```bash
python -m src.cli.create_data.create_data biorxiv \
      --start_date=2022-05-05 \
      --email=your.email@company.acme
```

Same as above for Medrxiv.
```bash
python -m src.cli.create_data.create_data medrxiv \
      --start_date=2022-04-01 \
      --email=your.email@company.acme
```

Retrieve the entire metadata available since April 2022 and also the source XML text.
```bash
python -m src.cli.create_data.create_data biorxiv \
      --start_date=2022-04-01 \
      --email=your.email@company.acme \
      --xml=True
```
### Using biotxiv-retriever as a python module

The functionalities of biorxiv-retriever can be used as normal python modules
in case it is necessary. 

```python


```