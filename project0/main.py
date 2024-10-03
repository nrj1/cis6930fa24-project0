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

# Function to create the database and incidents table
# def create_db(db_name):
#     # Full path to the database in the resources directory
#     db_path = os.path.join('C:/Users/Rajeev/Desktop/Git-Hub Projects/cis6930fa24-project0/resources', db_name)
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Drop table incidents if it exists as it has old data
#     cursor.execute('''DROP TABLE IF EXISTS incidents''')
#     # Create the incidents table
#     cursor.execute('''CREATE TABLE incidents (
#         incident_time TEXT,
#         incident_number TEXT,
#         incident_location TEXT,
#         nature TEXT,
#         incident_ori TEXT
#     )''')

#     conn.commit()
#     conn.close()
#     print(f"Database '{db_name}' and table 'incidents' created successfully.")

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




# def parse_incident_data(text):
#     pattern = re.compile(r'^(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2})\s+(\d{4}-\d{8})\s+([A-Z0-9 /.-]+)\s+([A-Z][a-z]+[A-Z][a-z]+)*)\s+([A-Z0-9]+)$')

#     special_natures = [
#         "Contact a Subject",
#         "Hit and Run",
#         "Runaway or Lost Child",
#         "MVA With Injuries",
#     ]

#     incidents = []
#     for line in text.splitlines():
#         match = pattern.match(line)
#         if match:
#             date_time = match.group(1)
#             incident_number = match.group(2)
#             rest_of_line = match.group(3)
#             incident_ori = match.group(4)

#             # Split the rest of the line into words
#             words = rest_of_line.split()

#             # Initialize variables
#             location = []
#             nature = []
#             nature_started = False

#             for word in words:
#                 if nature_started:
#                     nature.append(word)
#                 elif any(c.islower() for c in word) or word in ['MVA', 'EMS', 'COP', 'DDACTS', '911']:
#                     nature_started = True
#                     if word == 'MVA' and location and location[-1].endswith('MVA'):
#                         location[-1] = location[-1][:-3].strip()
#                     nature.append(word)
#                 else:
#                     location.append(word)

#             location = ' '.join(location)
#             nature = ' '.join(nature)

#             # Handle special cases
#             if nature == 'Breathing Problems 1400':
#                 nature = 'Breathing Problems'
#             elif nature == 'Assault EMS Needed 1400':
#                 nature = 'Assault EMS Needed'
#             elif nature == 'RAMPMotorist Assist':
#                 nature = 'Motorist Assist'
#             elif nature == 'Sick Person 1400':
#                 nature = 'Sick Person'

#             # Check if the nature is one of the special cases or follows the title case format
#             if nature in special_natures or all(word[0].isupper() and word[1:].islower() for word in nature.split()):
#                 incidents.append((date_time, incident_number, location, nature, incident_ori))

#     return incidents


# def populate_db(db_name, incidents):
#     # Full path to the database in the resources directory
#     db_path = os.path.join('C:/Users/Rajeev/Desktop/Git-Hub Projects/cis6930fa24-project0/resources', db_name)
    
#     # Connect to the database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Insert the list of incidents into the incidents table
#     cursor.executemany('''INSERT INTO incidents (incident_time, incident_number, incident_location, nature, incident_ori)
#                           VALUES (?, ?, ?, ?, ?)''', incidents)
    
#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()
    
#     print(f"Database '{db_name}' populated with {len(incidents)} records.")

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



# def status(db_path = 'C:/Users/Rajeev/Desktop/Git-Hub Projects/cis6930fa24-project0/resources/normanpd.db'):
    
#     # Connect to the database
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
    
#     # Insert the list of incidents into the incidents table
#     cursor.execute('''SELECT nature, COUNT(*) FROM incidents GROUP BY nature ORDER BY nature ASC''')
#     results = cursor.fetchall()

#     for row in results:
#         print(f"{row[0]} | {row[1]}")
        
    
#     # Commit the changes and close the connection
#     conn.commit()
#     conn.close()

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

# # Main code
# # Prompt for date input
# '''x = input("Enter date in yyyy-mm-dd format: ")
# y = x
# x = x[0:7] + "/" + x

# # Construct the URL
# url = "https://www.normanok.gov/sites/default/files/documents/" + x + "_daily_incident_summary.pdf"
# print(url)
# '''
# parser = argparse.ArgumentParser()
# parser.add_argument("--incidents", type=str, required=True, help="Incident summary url.")
     
# args = parser.parse_args()
# if args.incidents:
#     fetchincidents(args.incidents, "my_downloaded_file.pdf")
# else:
#     print("Enter valid arguments")

# # Fetch and save the PDF
# #fetchincidents(url, "my_downloaded_file_" + y + "_.pdf")

# # Extract text from the downloaded PDF
# #pdf_text = extract_text_from_pdf("my_downloaded_file_" + y + "_.pdf")
# pdf_text = extract_text_from_pdf("my_downloaded_file.pdf")
# print(pdf_text)

# # Create the database
# create_db("normanpd.db")

# # Parse the extracted PDF text and convert it to a list of incidents
# incidents = parse_incident_data(pdf_text)
# print(incidents)

# populate_db("normanpd.db", incidents)
# status()


# #and "incidents" in args.incidents 