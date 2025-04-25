from fastapi import FastAPI, UploadFile

from config import Config

app = FastAPI()


@app.get(f"{Config.API_ROOT}datasets/")
def list_dataset():
    """
    List all datasets.
    :return: A list of datasets
    """


@app.post(f"{Config.API_ROOT}datasets/")
def create_dataset(file: UploadFile):
    """
    Create a new dataset.
    :return: The dataset id
    """


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/")
def read_dataset(dataset_id: str):
    """
    Get the metadata (id, size) of a dataset.
    :param dataset_id: The dataset id
    :return: The dataset metadata
    """


@app.delete(f"{Config.API_ROOT}datasets/{{dataset_id}}/")
def delete_dataset(dataset_id: str):
    """
    Delete a dataset.
    :param dataset_id: The dataset id
    """


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/excel/")
def read_dataset_excel(dataset_id: str):
    """
    Get the dataset in Excel format.
    :param dataset_id: The dataset id
    :return: An Excel file, containing the dataset
    """


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/stats/")
def read_dataset_stats(dataset_id: str):
    """
    Get the dataset stats.
    :param dataset_id: The dataset id
    :return: The dataset stats
    """


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/plot/")
def read_dataset_plot(dataset_id: str):
    """
    Get the dataset plot.
    :param dataset_id: The dataset id
    :return: A PDF file containing a list of histograms of all the numerical columns in the dataset
    """


worker = FastAPI()


@worker.post("/parse/")
def parse_dataset(file: UploadFile):
    """
    Parse a csv file to a pandas dataframe, and save it to a file named by its generated id (UUID).
    :return: The dataset id
    """
