import typer
from rich.console import Console
from rich.table import Table

from pathlib import Path
from typing import Optional

import httpx

app = typer.Typer()
console = Console()

default_endpoint = "http://localhost:8000/datasets/"

@app.callback()
def global_options(
    endpoint: str = typer.Option(default_endpoint, help="Override API endpoint")
):
    app.endpoint = endpoint

@app.command()
def list():
    """List all uploaded datasets"""
    r = httpx.get(app.endpoint)
    if r.status_code != 200:
        raise ValueError(f"Failed to list datasets: {r.text}")
    datasets = r.json()
    if not datasets:
        print("No datasets found")
        return
    table = Table(title="Datasets")
    table.add_column("ID", justify="left", style="cyan")
    table.add_column("Name", justify="left", style="magenta")
    table.add_column("Size", justify="right", style="green")

    for dataset in datasets:
        table.add_row(
            dataset["id"],
            dataset.get("name", "Unnamed"),
            str(dataset.get("size", 0)) + " rows"
        )

    console.print(table)


@app.command()
def upload(csv_file: Path):
    """Upload a CSV file as a new dataset"""
    if not csv_file.exists():
        raise ValueError(f"File {csv_file} does not exist")
    with open(csv_file, "rb") as f:
        r = httpx.post(app.endpoint, files={"file": (csv_file.name, f, "text/csv")})
    if r.status_code != 200:
        raise ValueError(f"Failed to upload dataset: {r.text}")
    dataset_id = r.json().get("id")
    if dataset_id is None:
        raise ValueError("Failed to upload dataset: no id returned")
    print(f"Dataset {dataset_id} uploaded successfully")


def retrieve_file(url: str, file_path: Path):
    """Helper function to download a file from a URL"""
    r = httpx.get(url)
    if r.status_code != 200:
        raise ValueError(f"Failed to download file: {r.text}")
    with open(file_path, "wb") as f:
        f.write(r.content)
    print(f"File saved to {file_path}")

@app.command()
def get(
    dataset_id: str,
    info: bool = typer.Option(False, "--info", help="Return metadata (default)"),
    stats: bool = typer.Option(False, "--stats", help="Return df.describe() as JSON"),
    excel: Optional[Path] = typer.Option(None, "--excel", help="Download Excel version"),
    plot: Optional[Path] = typer.Option(None, "--plot", help="Download histogram PDF")
):
    """
    Get dataset metadata, stats, or derived files
    """
    processed = False

    if stats:
        r = httpx.get(f"{app.endpoint}{dataset_id}/stats/")
        if r.status_code != 200:
            raise ValueError(f"Failed to get dataset stats: {r.text}")
        stats = r.json()
        print(stats)
        processed = True

    if excel is not None:
        retrieve_file(f"{app.endpoint}{dataset_id}/excel/", excel)
        processed = True

    if plot is not None:
        retrieve_file(f"{app.endpoint}{dataset_id}/plot/", plot)
        processed = True

    if info or not processed:
        r = httpx.get(f"{app.endpoint}{dataset_id}/")
        if r.status_code != 200:
            raise ValueError(f"Failed to get dataset info: {r.text}")
        dataset_info = r.json()
        print(dataset_info)

@app.command()
def delete(dataset_id: str):
    """Delete a dataset"""
    r = httpx.delete(f"{app.endpoint}{dataset_id}/")
    if r.status_code != 200:
        raise ValueError(f"Failed to delete dataset: {r.text}")
    print(f"Dataset {dataset_id} deleted successfully")

if __name__ == "__main__":
    app()
