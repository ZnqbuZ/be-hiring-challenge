import shutil
import httpx

from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

from config import Config, logger
from dataset import Dataset, DatasetStream

app = FastAPI()


@app.get(f"{Config.API_ROOT}datasets/")
def list_dataset():
    """
    List all datasets.
    :return: A list of datasets
    """

    logger.info("Listing datasets")
    for dataset_dir in Config.FILE_STORE.iterdir():
        if dataset_dir.is_dir():
            try:
                dataset = Dataset(id=dataset_dir.name)
                yield dataset.info
            except ValueError:
                logger.warning(f"Dataset {dataset_dir.name} is not a valid dataset")


@app.post(f"{Config.API_ROOT}datasets/")
def create_dataset(file: UploadFile):
    """
    Create a new dataset.
    :return: The dataset id
    """

    logger.info("Creating new dataset")
    if file is None:
        raise ValueError("file is required")

    r = httpx.post(Config.WORKER_ENDPOINT + "/parse/", files={"file": (file.filename, file.file, file.content_type)})
    if r.status_code != 200:
        raise ValueError(f"Failed to create dataset: {r.text}")
    dataset_id = r.json().get("id")
    if dataset_id is None:
        raise ValueError("Failed to create dataset: no id returned")
    return {"id": dataset_id}


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/")
def read_dataset(dataset_id: str):
    """
    Get the metadata (id, size) of a dataset.
    :param dataset_id: The dataset id
    :return: The dataset metadata
    """

    logger.info(f"Getting dataset {dataset_id}")
    dataset = Dataset(id=dataset_id)
    return dataset.info


@app.delete(f"{Config.API_ROOT}datasets/{{dataset_id}}/")
def delete_dataset(dataset_id: str):
    """
    Delete a dataset.
    :param dataset_id: The dataset id
    """

    logger.info(f"Deleting dataset {dataset_id}")
    path = Config.FILE_STORE / dataset_id
    if path.exists():
        shutil.rmtree(path)
    else:
        raise ValueError(f"Dataset {dataset_id} not found")


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/excel/")
def read_dataset_excel(dataset_id: str):
    """
    Get the dataset in Excel format.
    :param dataset_id: The dataset id
    :return: An Excel file, containing the dataset
    """

    logger.info(f"Getting dataset {dataset_id} in Excel format")
    dataset = Dataset(id=dataset_id)

    return StreamingResponse(dataset.s_iter(DatasetStream.EXCEL),
                             media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/stats/")
def read_dataset_stats(dataset_id: str):
    """
    Get the dataset stats.
    :param dataset_id: The dataset id
    :return: The dataset stats
    """

    logger.info(f"Getting dataset {dataset_id} stats")
    dataset = Dataset(id=dataset_id)
    return dataset.stats.to_json(orient="records", indent=4)


@app.get(f"{Config.API_ROOT}datasets/{{dataset_id}}/plot/")
def read_dataset_plot(dataset_id: str):
    """
    Get the dataset plot.
    :param dataset_id: The dataset id
    :return: A PDF file containing a list of histograms of all the numerical columns in the dataset
    """

    logger.info(f"Getting dataset {dataset_id} plot")
    dataset = Dataset(id=dataset_id)
    return StreamingResponse(dataset.s_iter(DatasetStream.PLOT), media_type="application/pdf")


worker = FastAPI()


@worker.post("/parse/")
def parse_dataset(file: UploadFile):
    """
    Parse a csv file to a pandas dataframe, and save it to a file named by its generated id (UUID).
    :return: The dataset id
    """

    logger.info("Parsing dataset")
    if file is None:
        raise ValueError("file is required")

    dataset = Dataset(file.file, mode="csv", name=file.filename)
    dataset.save()
    return {"id": str(dataset.id)}
