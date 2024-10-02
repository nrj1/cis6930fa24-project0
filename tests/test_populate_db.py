'''import sqlite3
import os
from project0.main import create_db, populate_db


def test_populate_db():
    db_name = "test_db.db"
    
    # Create the database
    create_db(db_name)
    
    # Sample incident data
    incidents = [
        ('8/1/2024 0:04', '2024-00055419', '1345 W LINDSEY ST', 'Traffic Stop', 'OK0140200'),
        ('8/1/2024 0:15', '2024-00055420', '1600 E LINDSEY ST', 'Burglary', 'OK0140200')
    ]
    
    # Populate the database
    populate_db(db_name, incidents)
    
    # Verify the records are inserted
    db_path = os.path.join('C:/Users/Rajeev/Desktop/Git-Hub Projects/cis6930fa24-project0/resources', db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    records = cursor.fetchall()
    
    assert len(records) == 2, "Records were not inserted correctly"
    
    # Clean up
    conn.close()
    os.remove(db_path)'''

import sqlite3
import os
from project0.main import create_db, populate_db

def test_populate_db():
    db_name = "test_db.db"
    
    # Get the path to the resources directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, 'resources')

    # Ensure resources directory exists
    os.makedirs(resources_dir, exist_ok=True)
    
    # Full path to the database
    db_path = os.path.join(resources_dir, db_name)
    
    # Create the database
    create_db(db_path)
    
    # Sample incident data
    incidents = [
        ('8/1/2024 0:04', '2024-00055419', '1345 W LINDSEY ST', 'Traffic Stop', 'OK0140200'),
        ('8/1/2024 0:15', '2024-00055420', '1600 E LINDSEY ST', 'Burglary', 'OK0140200')
    ]
    
    # Populate the database
    populate_db(db_path, incidents)
    
    # Verify the records are inserted
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents")
    records = cursor.fetchall()
    
    assert len(records) == 2, "Records were not inserted correctly"
    
    # Clean up
    conn.close()
    os.remove(db_path)