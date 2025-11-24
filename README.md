# BoundaryML PDF parsing workspace

This repository contains tools and experiments for extracting tables from PDFs/images using the BoundaryML-generated client and a small analysis notebook.

Contents
- main.py — example entry point for using the generated client
- play.ipynb — interactive notebook used to extract pages, parse LLM responses and compare against ground truth
- sample_tables.pdf / sample_tables.png — sample inputs used by the notebook
- img_results.csv / pdf_results.csv — recorded LLM call results used by the analysis
- baml_client/ — generated Python client (Pydantic models, parser, and helpers)
- baml_src/ — source .baml files used to generate the client

Quick setup (using uv)
1. Initialize the uv workspace (if not already done):
   uv init

2. Add required runtime packages to the project via uv. Example packages used by the notebook and scripts:
   uv add baml-py
   uv add pypdf2 pdf2image pillow pandas fuzzywuzzy pydantic

   Notes:
   - pdf2image requires Poppler installed on your system. On macOS:
     brew install poppler
   - fuzzywuzzy has an optional speedup (python-Levenshtein). Add it if desired:
     uv add python-Levenshtein

Ensure that the ANTHROPIC_API_KEY is set in a .env file.

Follow (guide)[https://docs.boundaryml.com/guide/installation-language/python] to setup BAML
```
uv init
uv add baml-py
uv run baml-cli init
```

Update the clients.baml & resume.baml and execute in baml_src directory to reflect goals of the project.

Users can make sync or async client calls using main.py.

Generate the Python client (BAML)
- The baml_client package is generated from the .baml files in baml_src.
- To (re)generate the client run the BoundaryML CLI in the baml_src directory:

  uv run baml-cli generate

Pydantic models are generated from .baml files. If you set up the VSCode extention then it will automatically run baml-cli generate on saving a BAML file. This assumes you have the `uv` tooling from BoundaryML installed and configured.

Notebook (play.ipynb)
- The notebook contains end-to-end examples:
  - extract_page_to_png: extract a PDF page and convert to PNG (PyPDF2 + pdf2image)
  - parsing LLM responses into Pydantic Table models using a safe parser (regex + ast.literal_eval)
  - computing fuzzy match ratios against ground-truth tables and summarising results in CSVs
- To run the notebook:
  uv run jupyter lab play.ipynb

Important files for tests/examples
- test_song_collection_table.png and test_song_collection_table.pdf — test assets included in the repo (some may contain embedded base64 data used by tests).
- img_results.csv and pdf_results.csv — recorded LLM responses used by the analysis cells in the notebook.

Development notes
- The code avoids using eval on untrusted input; the notebook shows a safe parsing approach using regex + ast.literal_eval when converting string representations of Table(...) into Pydantic models.
- If you need to add or update models, edit the .baml files in baml_src and re-run the generator.

## Test Cases
test_song_collection_table.png has base64 encoding

test_song_collection_table.pdf has base64 encoding