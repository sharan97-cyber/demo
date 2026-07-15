import pytest
import json
import os
from app import process_data, write_output

def test_process_data():
    """Test that process_data returns valid structure"""
    data = process_data()
    assert data["status"] == "success"
    assert data["items_processed"] == 42
    assert "timestamp" in data

def test_write_output(tmp_path):
    """Test that write_output creates file"""
    os.chdir(tmp_path)
    data = {"test": "data"}
    write_output(data)
    
    output_file = tmp_path / "output.json"
    assert output_file.exists()
    
    with open(output_file) as f:
        content = json.load(f)
    assert content["test"] == "data"

def test_output_file_format():
    """Test output file has valid JSON format"""
    data = process_data()
    write_output(data)
    
    with open("output.json") as f:
        content = json.load(f)
    assert isinstance(content, dict)
    assert "timestamp" in content
