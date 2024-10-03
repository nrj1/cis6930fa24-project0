# CIS6930FA24 -- Project 0 

Name: Neil Rajeev John 

## Project Description This project involves creating a Python package that fetches incident data from the Norman, Oklahoma Police Department, processes it, and stores it in a SQLite database. The package includes functionality to download PDF reports, extract text from PDFs, create and populate a database, and display incident statistics.

## How to Install To install the package, use the following command:

pipenv install

## How to Run To run the program, use the following command:

pipenv run python project0/main.py --incidents <URL_TO_INCIDENT_SUMMARY>

Replace `<URL_TO_INCIDENT_SUMMARY>` with the actual URL of the incident summary PDF. ![Demo Video](path_to_your_demo_video.gif)

## Functions ### 

main.py 

- `fetchincidents(url, filename)`: Downloads a PDF from the given URL and saves it to the tmp folder. 

- `extract_text_from_pdf(filename)`: Extracts text content from a PDF file. 

- `create_db(db_name)`: Creates a SQLite database with an 'incidents' table. 

- `parse_incident_data(text)`: Parses incident data from extracted text using regex. 

- `populate_db(db_name, incidents)`: Populates the database with parsed incident data. 

- `status(db_name='normanpd.db')`: Displays incident statistics from the database. 

- `main(url)`: Orchestrates the entire process from fetching to displaying statistics.

## Database Development The database is developed using SQLite. It consists of a single table named 'incidents' with columns for incident time, number, location, nature, and ORI. The database is created in the 'resources' directory, which is automatically created if it doesn't exist.

## Test Files The project includes several test files to ensure the functionality of key components: 

### test_fetchincidents.py This test file verifies the `fetchincidents()` function: 

- It mocks the URL request and response to simulate downloading a PDF. 

- Checks if the file is saved in the correct location (tmp folder). 

- Ensures the correct data is written to the file. 

### test_extractincidents.py Tests the `extract_text_from_pdf()` function: 

- Creates a dummy PDF file with known content. 

- Extracts text from the dummy PDF. 

- Verifies if the extracted text matches the original content. 

### test_createdb.py Validates the `create_db()` function: 

- Creates a test database. 

- Checks if the database file is created in the correct location. 

- Verifies if the 'incidents' table is properly created in the database.

### test_populate_db.py 

Tests the `populate_db()` function: 

- Creates a test database. 

- Populates it with sample incident data. 

- Verifies if the correct number of records are inserted into the database. 

### test_status.py 

Checks the `status()` function: 

- Creates a test database with sample incident data. 

- Calls the status function and captures its output. 

- Verifies if the output correctly represents the incident statistics.

These tests ensure that each component of the project functions as expected, from fetching and processing PDF data to database operations and status reporting. They use mock objects and temporary files to isolate the testing environment and prevent interference with actual system resources. To run the tests, use the following command:

pipenv run pytest

This will execute all test files and report the results, helping to maintain the reliability and correctness of the project's core functionalities.

## Bugs and Assumptions 

1\. The `parse_incident_data()` function assumes that the location column in the incident data contains only characters A-Z, 0-9, and '. /;-', excluding lowercase alphabets. 

2\. The nature column in the incident data usually follows a pattern of having the first letter of each word capitalized. However, there are exceptions like 'MVA Non Injury' and 'COP DDACTS' which may not follow this pattern consistently. 

3\. The program assumes a specific directory structure with 'tmp' and 'resources' folders at the same level as the 'project0' folder. 

4\. The PDF structure is assumed to be consistent for text extraction.

## Installation and Usage 

1\. Ensure you have Python 3.10 installed. 

2\. Install pipenv if not already installed: `pip install pipenv` 

3\. Clone the repository and navigate to the project directory. 

4\. Run `pipenv install` to set up the virtual environment and install dependencies. 

5\. Use the command mentioned in the "How to Run" section to execute the program. Note: This code is original and not copied from any unauthorized sources.