To run this client, `uv` is required. See [the official website](https://docs.astral.sh/uv/getting-started/installation/) for an installation guide.
After `uv` is installed, run `uv run python main.py --help` in directory `client` to see avaliable commands.

Examples:

```
uv run python main.py list --endpoint http://127.0.0.1:8000/datasets/

uv run python main.py upload ../sample_data_2.csv

uv run python main.py get --help

uv run python main.py get d912131a-74dd-471e-bf05-2bee592d3239 --excel excel.xlsx
```
