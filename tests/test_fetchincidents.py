# import os
# import urllib.request
# from unittest import mock
# from project0.main import fetchincidents

# def test_fetchincidents():
#     url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-11_daily_incident_summary.pdf"
#     filename = "test_file.pdf"

#     # Mock the response of urlopen
#     mock_response = mock.Mock()
#     mock_response.read.return_value = b"%PDF-1.4 test pdf data"
    
#     with mock.patch('urllib.request.urlopen', return_value=mock_response):
#         fetchincidents(url, filename)
        
#     # Verify that the file was created
#     filepath = os.path.join(r"C:\Users\Rajeev\Desktop\Git-Hub Projects\cis6930fa24-project0\tmp", filename)
#     assert os.path.exists(filepath), "File was not downloaded correctly"
    
#     # Clean up the created file
#     os.remove(filepath)

import os
from unittest import mock
from project0.main import fetchincidents

def test_fetchincidents():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-08/2024-08-11_daily_incident_summary.pdf"
    filename = "test_file.pdf"

    # Create a mock context manager
    mock_cm = mock.MagicMock()
    mock_cm.__enter__.return_value = mock.MagicMock()
    mock_cm.__enter__.return_value.read.return_value = b"%PDF-1.4 test pdf data"

    with mock.patch('project0.main.urllib.request.Request') as mock_request, \
         mock.patch('project0.main.urllib.request.urlopen', return_value=mock_cm) as mock_urlopen, \
         mock.patch('project0.main.open', mock.mock_open()) as mock_file:

        fetchincidents(url, filename)
        
        # Assert that urlopen was called with the correct request object
        mock_urlopen.assert_called_once()
        
        # Assert that the file was opened for writing
        expected_filepath = os.path.join(r"C:\Users\Rajeev\Desktop\Git-Hub Projects\cis6930fa24-project0\tmp", filename)
        mock_file.assert_called_once_with(expected_filepath, 'wb')
        
        # Assert that write was called on the file with the correct data
        mock_file().write.assert_called_once_with(b"%PDF-1.4 test pdf data")
