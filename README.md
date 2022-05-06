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


### Using biotxiv-retriever as a python module

