import typer

from pathlib import Path
from typing import Optional

app = typer.Typer()

default_endpoint = "http://localhost:8000/datasets/"

@app.callback()
def global_options(
    endpoint: str = typer.Option(default_endpoint, help="Override API endpoint")
):
    app.endpoint = endpoint

@app.command()
def list():
    """List all uploaded datasets"""
    pass

@app.command()
def upload(csv_file: Path):
    """Upload a CSV file as a new dataset"""
    pass

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
    pass

@app.command()
def delete(dataset_id: str):
    """Delete a dataset"""
    pass

if __name__ == "__main__":
    app()
