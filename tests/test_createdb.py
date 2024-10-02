'''import os
import sqlite3
from project0.main import create_db

def test_create_db():
    db_name = "test_db.db"
    
    # Create the database
    create_db(db_name)
    
    # Check if the database file exists
    db_path = os.path.join('C:/Users/Rajeev/Desktop/Git-Hub Projects/cis6930fa24-project0/resources', db_name)
    assert os.path.exists(db_path), "Database file not created"
    
    # Check if the table is created
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table_exists = cursor.fetchone()
    
    assert table_exists is not None, "Table 'incidents' not created"
    
    # Clean up
    conn.close()
    os.remove(db_path)
    '''

import os
import sqlite3
from project0.main import create_db

def test_create_db():
    db_name = "test_db.db"
    
    # Get the path to the resources directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, 'resources')

    # Ensure resources directory exists
    os.makedirs(resources_dir, exist_ok=True)
    
    # Create the database
    create_db(os.path.join(resources_dir, db_name))
    
    # Check if the database file exists
    db_path = os.path.join(resources_dir, db_name)
    assert os.path.exists(db_path), "Database file not created"
    
    # Check if the table is created
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    table_exists = cursor.fetchone()
    
    assert table_exists is not None, "Table 'incidents' not created"
    
    # Clean up
    conn.close()
    os.remove(db_path)
