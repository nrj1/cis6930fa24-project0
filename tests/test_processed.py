import pytest
import sqlite3
import os
import sys
from unittest.mock import patch, MagicMock
from io import BytesIO

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from project0.main import (
    IncidentRecord, fetch_and_parse_pdf, extract_incidents_from_page,
    setup_database, populate_database, generate_nature_report, process_incidents
)

# Update the DB_NAME to reflect the correct path
DB_NAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resources", "normanpd.db")

@pytest.fixture
def sample_pdf_content():
    return b"%PDF-1.3\n...sample PDF content..."

@pytest.fixture
def mock_pdf_reader(sample_pdf_content):
    with patch('project0.main.PdfReader') as mock_reader:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = (
            "1/1/2023 12:00 2023-00001    123 Main St    Theft    NORM0123\n"
            "1/2/2023 13:00 2023-00002    456 Elm St     Assault  NORM0124\n"
            "1/3/2023 14:00 2023-00003    789 Oak St              NORM0125"
        )
        mock_reader.return_value.pages = [mock_page]
        yield mock_reader

@pytest.fixture
def test_db_path(tmp_path):
    db_path = tmp_path / "normanpd.db"
    yield str(db_path)
    if os.path.exists(db_path):
        os.remove(db_path)

def test_incident_record():
    incident = IncidentRecord("1/1/2023 12:00", "2023-00001", "123 Main St", "Theft", "NORM0123")
    assert incident.time == "1/1/2023 12:00"
    assert incident.number == "2023-00001"
    assert incident.location == "123 Main St"
    assert incident.nature == "Theft"
    assert incident.ori == "NORM0123"

# def test_fetch_and_parse_pdf(mock_pdf_reader, sample_pdf_content):
#     with patch('project0.main.requests.get') as mock_get:
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.content = sample_pdf_content
        
#         incidents = fetch_and_parse_pdf("https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-03_daily_arrest_summary.pdf")
        
#         assert len(incidents) == 3
#         assert isinstance(incidents[0], IncidentRecord)
#         assert incidents[0].time == "1/1/2023 12:00"
#         assert incidents[2].nature == ""  # Test for incident with missing fields

# def test_extract_incidents_from_page():
#     mock_page = MagicMock()
#     mock_page.extract_text.return_value = (
#         "1/1/2023 12:00 2023-00001    123 Main St    Theft    NORM0123\n"
#         "1/2/2023 13:00 2023-00002    456 Elm St     Assault  NORM0124\n"
#         "1/3/2023 14:00 2023-00003    789 Oak St              NORM0125"
#     )
    
#     incidents = extract_incidents_from_page(mock_page)
    
#     assert len(incidents) == 3
#     assert incidents[0].nature == "Theft"
#     assert incidents[2].nature == ""

def test_setup_database(test_db_path):
    with patch('project0.main.DB_NAME', test_db_path):
        conn = setup_database()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='police_incidents'")
        assert cursor.fetchone() is not None
        
        conn.close()

def test_populate_database(test_db_path):
    with patch('project0.main.DB_NAME', test_db_path):
        conn = setup_database()
        incidents = [
            IncidentRecord("1/1/2023 12:00", "2023-00001", "123 Main St", "Theft", "NORM0123"),
            IncidentRecord("1/2/2023 13:00", "2023-00002", "456 Elm St", "Assault", "NORM0124")
        ]
        
        populate_database(conn, incidents)
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM police_incidents")
        assert cursor.fetchone()[0] == 2
        
        conn.close()

def test_generate_nature_report(test_db_path):
    with patch('project0.main.DB_NAME', test_db_path):
        conn = setup_database()
        incidents = [
            IncidentRecord("1/1/2023 12:00", "2023-00001", "123 Main St", "Theft", "NORM0123"),
            IncidentRecord("1/2/2023 13:00", "2023-00002", "456 Elm St", "Assault", "NORM0124"),
            IncidentRecord("1/3/2023 14:00", "2023-00003", "789 Oak St", "Theft", "NORM0125")
        ]
        populate_database(conn, incidents)
        
        report = generate_nature_report(conn)
        
        assert len(report) == 2
        assert report[0] == ("Theft", 2)
        assert report[1] == ("Assault", 1)
        
        conn.close()

# def test_process_incidents(mock_pdf_reader, sample_pdf_content, test_db_path, capsys):
#     with patch('project0.main.DB_NAME', test_db_path), \
#          patch('project0.main.requests.get') as mock_get:
#         mock_get.return_value.status_code = 200
#         mock_get.return_value.content = sample_pdf_content
        
#         process_incidents("https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-03_daily_arrest_summary.pdf")
        
#         captured = capsys.readouterr()
#         assert "Theft|1" in captured.out
#         assert "Assault|1" in captured.out

def test_process_incidents_error_handling(capsys):
    with patch('project0.main.requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        
        process_incidents("https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-03_daily_arrest_summary.pdf")
        
        captured = capsys.readouterr()
        assert "An error occurred: Failed to fetch PDF from URL" in captured.out