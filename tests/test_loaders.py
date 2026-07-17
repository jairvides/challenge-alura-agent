import pytest
from src.utils.loaders import load_document, load_all_documents
import os

def test_load_markdown():
    path = "data/privacy_policy.md"
    docs = load_document(path)
    assert len(docs) > 0
    assert "Privacy Policy" in docs[0].page_content

def test_load_csv():
    path = "data/shipping_guide.csv"
    docs = load_document(path)
    assert len(docs) > 0
    assert "region" in docs[0].page_content

def test_load_json():
    path = "data/faq.json"
    docs = load_document(path)
    assert len(docs) > 0
    assert "return a product" in str(docs)

def test_load_all_documents():
    docs = load_all_documents("data")
    assert len(docs) >= 3
