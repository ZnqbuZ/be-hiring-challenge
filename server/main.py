import os
from typing import Union

from fastapi import FastAPI

api_root = os.environ.get("API_ROOT", "/")
worker_host = os.environ.get("WORKER", "dataset-worker")


app = FastAPI()

@app.get(f"${api_root}datasets/")
def list_dataset():
    """
    List all datasets.
    :return: A list of datasets
    """
    pass


@app.post(f"${api_root}datasets/")
def create_dataset(request_body: Union[None, dict] = None):
    """
    Create a new dataset.
    :return: The dataset id
    """
    pass


@app.get(f"${api_root}datasets/{{dataset_id}}/")
def read_dataset(dataset_id: str):
    """
    Get the metadata (id, size) of a dataset.
    :param dataset_id: The dataset id
    :return: The dataset metadata
    """
    pass


@app.delete(f"${api_root}datasets/{{dataset_id}}/")
def delete_dataset(dataset_id: str):
    """
    Delete a dataset.
    :param dataset_id: The dataset id
    """
    pass


@app.get(f"${api_root}datasets/{{dataset_id}}/excel/")
def read_dataset_excel(dataset_id: str):
    """
    Get the dataset in Excel format.
    :param dataset_id: The dataset id
    :return: An Excel file, containing the dataset
    """
    pass


@app.get(f"${api_root}datasets/{{dataset_id}}/stats/")
def read_dataset_stats(dataset_id: str):
    """
    Get the dataset stats.
    :param dataset_id: The dataset id
    :return: The dataset stats
    """
    pass


@app.get(f"${api_root}datasets/{{dataset_id}}/plot/")
def read_dataset_plot(dataset_id: str):
    """
    Get the dataset plot.
    :param dataset_id: The dataset id
    :return: A PDF file containing a list of histograms of all the numerical columns in the dataset
    """
    pass

worker = FastAPI()

@worker.post("/parse/")
def parse_dataset(request_body: Union[None, dict] = None):
    """
    Parse a csv file to a pandas dataframe, and save it to a file named by its generated id (UUID).
    :return: The dataset id
    """
    pass

