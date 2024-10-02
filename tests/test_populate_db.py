import sqlite3
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
    os.remove(db_path)
