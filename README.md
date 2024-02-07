# PDF Content Search App

This application allows users to upload PDF files, enter a search query, and receive relevant text snippets from the PDF as search results.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Python 3.8 or higher (if running outside Docker)

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

1. Clone the repository to your local machine.
2. Navigate to the cloned directory.

#### Using Docker

```bash
docker build -t pdf-search-app .
docker run -p 8501:8501 pdf-search-app
```

#### Without Docker

```bash
git clone https://github.com/abdullah-alnahas/pdf-ai/
cd pdf-ai
pip install poetry==1.7.1
poetry install
poetry run streamlit run app.py
```


## Using the App

1. Navigate to `http://localhost:8501` in your web browser.
2. Upload a PDF file using the file uploader.
3. Enter your search query in the text box.
4. Click on the "Search" button to perform the search.
5. View the search results displayed on the page.

## Built With

* [Streamlit](https://www.streamlit.io/) - The web framework used
* [Qdrant](https://qdrant.tech/) - Vector search engine for embedding storage and search
* [Docker](https://www.docker.com/) - Containerization

## Authors

* Abdullah Al Nahas (BAKIRCI)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
