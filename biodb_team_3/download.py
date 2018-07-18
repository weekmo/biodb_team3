import requests

def download():
    """Function to download the latest version of the mapping between OMIM and uniprot."""
    url = 'http://www.uniprot.org/docs/mimtosp.txt'
    file_Name = 'data.txt'
    data = requests.get(url)
    file = open(file_Name, 'wb')
    for line in data.iter_content():
        file.write(line)
    file.close()

download()
