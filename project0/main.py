import sqlite3
import os
import urllib.request
from pypdf import PdfReader
import re
import argparse

# Function to fetch and save PDF from URL

def fetchincidents(url, filename):
    # Get the path to the tmp directory
    current_dir = os.path.dirname(os.path.abspath(__file__))  # project0 directory
    parent_dir = os.path.dirname(current_dir)  # parent directory containing project0 and tmp
    tmp_dir = os.path.join(parent_dir, 'tmp')
    
    # Ensure the tmp directory exists
    os.makedirs(tmp_dir, exist_ok=True)
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url, headers=headers)
    filepath = os.path.join(tmp_dir, filename)
    
    with urllib.request.urlopen(request) as response:
        data = response.read()
        # Save the PDF data to a file
        with open(filepath, 'wb') as file:
            file.write(data)
    print(f"PDF downloaded and saved as {filename} in tmp folder")

# Function to extract text from the downloaded PDF

def extract_text_from_pdf(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    tmp_dir = os.path.join(parent_dir, 'tmp')
    filepath = os.path.join(tmp_dir, filename)
    reader = PdfReader(filepath)
    text = "" 
    for page in reader.pages:
        text += page.extract_text()
    return text



def create_db(db_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, 'resources')
    os.makedirs(resources_dir, exist_ok=True)
    db_path = os.path.join(resources_dir, db_name)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE IF EXISTS incidents''')
    cursor.execute('''CREATE TABLE incidents (
        incident_time TEXT,
        incident_number TEXT,
        incident_location TEXT,
        nature TEXT,
        incident_ori TEXT
    )''')

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' and table 'incidents' created successfully.")


def parse_incident_data(text):
    # Regular expression to capture the data based on your pattern
    pattern = re.compile(r'(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2})\s+(\d{4}-\d{8})\s+([A-Z0-9. /;-]+)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+([A-Z0-9]+)$')


    incidents = []
    for line in text.splitlines():
        match = pattern.match(line)
        if match:
            date_time = match.group(1)
            incident_number = match.group(2)
            location = match.group(3)
            nature = match.group(4)
            incident_ori = match.group(5)
            # Append as a tuple or a list
            incidents.append((date_time, incident_number, location, nature, incident_ori))
    return incidents




def populate_db(db_name, incidents):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, 'resources')
    db_path = os.path.join(resources_dir, db_name)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.executemany('''INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
                          VALUES (?, ?, ?, ?, ?)''', incidents)
    
    conn.commit()
    conn.close()
    
    print(f"Database '{db_name}' populated with {len(incidents)} records.")



def status(db_name='normanpd.db'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    resources_dir = os.path.join(parent_dir, 'resources')
    db_path = os.path.join(resources_dir, db_name)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    #cursor.execute('''SELECT DISTINCT nature FROM incidents''')
    cursor.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC''')
    results = cursor.fetchall()

    for row in results:
        print(f"{row[0]} | {row[1]}")
        #print(f"{row[0]}")
    
    conn.close()    

def main(url):
    fetchincidents(url, "my_downloaded_file.pdf")
    pdf_text = extract_text_from_pdf("my_downloaded_file.pdf")
    print(pdf_text)
    create_db("normanpd.db")
    incidents = parse_incident_data(pdf_text)
    print(incidents)
    populate_db("normanpd.db", incidents)
    status()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
    else:
        print("Enter valid arguments")

