---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.17.3
  kernelspec:
    display_name: CSPLab Base (pandas, numpy, matplotlib)
    language: python
    name: csplab-base
---

# Notebook Elasticsearch integration example

This notebook aims to demonstrate how to query an elasticseach database running locally (using Docker).


## Getting started

```python
from elasticsearch import Elasticsearch

# Service name in the docker compose network
ELASTICSEARCH_URL = "http://elasticsearch:9200/"

# API client
client = Elasticsearch(ELASTICSEARCH_URL)
```

## Working with indexes

```python
# Create an index
client.indices.create(index="my_index")
```

```python
# Add a document to the index
client.index(
    index="my_index",
    id="my_document_id",
    document={
        "foo": "foo",
        "bar": "bar",
    }
)
```

```python
# Get indexed documents
client.get(index="my_index", id="my_document_id")
```

## Going further

This notebook uses examples from the [official documentation}(https://www.elastic.co/docs/reference/elasticsearch/clients/python). Feel free to explore it and to whatever you want with ES.
