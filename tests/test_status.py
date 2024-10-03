import sqlite3
import os
from project0.main import create_db, populate_db, status

def test_status(capsys):
    db_name = "test_db.db"
    
    # Get the path to the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Define paths relative to the project root
    resources_dir = os.path.join(project_root, 'resources')
    os.makedirs(resources_dir, exist_ok=True)
    db_path = os.path.join(resources_dir, db_name)
    
    # Ensure the database doesn't exist before the test
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create the database
    create_db(db_name)
    
    # Sample incident data
    incidents = [
        ('8/1/2024 0:04', '2024-00055419', '1345 W LINDSEY ST', 'Traffic Stop', 'OK0140200'),
        ('8/1/2024 0:15', '2024-00055420', '1600 E LINDSEY ST', 'Burglary', 'OK0140200'),
        ('8/1/2024 0:30', '2024-00055421', '123 MAIN ST', 'Burglary', 'OK0140201')
    ]
    
    # Populate the database
    populate_db(db_name, incidents)
    
    # Call the status function and capture its output
    status(db_path)
    
    captured = capsys.readouterr()
    print("Captured output:", captured.out)  # Add this line to see the actual output
    assert "Burglary | 2" in captured.out, "Status output is incorrect"
    assert "Traffic Stop | 1" in captured.out, "Status output is incorrect"
    
    # Clean up
    os.remove(db_path)