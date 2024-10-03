import io
import re
import requests
import sqlite3
import os
import argparse
from pypdf import PdfReader

class IncidentRecord:
    def __init__(self, time, number, location, nature, ori):
        self.time = time
        self.number = number
        self.location = location
        self.nature = nature
        self.ori = ori

    @classmethod
    def display_info(cls, record):
        for attr, value in record.__dict__.items():
            print(f"{attr}: {value}")

DB_NAME = "resources/normanpd.db"
CREATE_TABLE_QUERY = '''
CREATE TABLE IF NOT EXISTS police_incidents (
    incident_time TEXT,
    incident_number TEXT,
    incident_location TEXT,
    incident_nature TEXT,
    incident_ori TEXT
);
'''
INSERT_QUERY = '''
INSERT INTO police_incidents 
(incident_time, incident_number, incident_location, incident_nature, incident_ori)
VALUES (?, ?, ?, ?, ?)
'''
NATURE_COUNT_QUERY = '''
SELECT incident_nature, COUNT(*) as nature_count 
FROM police_incidents 
GROUP BY incident_nature 
ORDER BY nature_count DESC, 
    CASE WHEN incident_nature = '' THEN 1 ELSE 0 END, 
    incident_nature
'''

def fetch_and_parse_pdf(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch PDF from URL")
    
    pdf_reader = PdfReader(io.BytesIO(response.content))
    incidents = []
    
    for page in pdf_reader.pages:
        incidents.extend(extract_incidents_from_page(page))
    
    return incidents

def extract_incidents_from_page(page):
    text_content = page.extract_text(extraction_mode="layout", 
                                     layout_mode_space_vertically=False,
                                     layout_mode_scale_weight=2.0)
    lines = text_content.split("\n")
    page_incidents = []
    
    for line in lines:
        if line.strip() and not line.startswith("    "):
            fields = [field.strip() for field in re.split(r"\s{4,}", line.strip())]
            if len(fields) == 5:
                incident = IncidentRecord(*fields)
            elif len(fields) == 3:
                incident = IncidentRecord(fields[0], fields[1], "", "", fields[2])
            else:
                continue
            page_incidents.append(incident)
    
    return page_incidents

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS police_incidents")
    cursor.execute(CREATE_TABLE_QUERY)
    conn.commit()
    return conn

def populate_database(conn, incidents):
    cursor = conn.cursor()
    cursor.executemany(INSERT_QUERY, 
                       [(inc.time, inc.number, inc.location, inc.nature, inc.ori) 
                        for inc in incidents])
    conn.commit()

def generate_nature_report(conn):
    cursor = conn.cursor()
    cursor.execute(NATURE_COUNT_QUERY)
    return cursor.fetchall()

def process_incidents(url):
    try:
        incidents = fetch_and_parse_pdf(url)
        conn = setup_database()
        populate_database(conn, incidents)
        
        nature_report = generate_nature_report(conn)
        for nature, count in nature_report:
            print(f"{nature}|{count}")
        
        conn.close()
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process police incident reports")
    parser.add_argument("--incidents", type=str, required=True, 
                        help="URL of the incident summary PDF")
    args = parser.parse_args()
    
    if args.incidents:
        process_incidents(args.incidents)
    else:
        print("Please provide a valid incident summary URL")