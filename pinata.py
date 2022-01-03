from dotenv.main import dotenv_values
import requests
import os

env_config = dotenv_values(".env")

def pinata_upload(filename=None, test=False):
    test_url = 'https://api.pinata.cloud/data/testAuthentication';
    test_headers = {
        'pinata_api_key': env_config["IPFS_API_Key"],
        'pinata_secret_api_key': env_config["IPFS_API_Secret"]
    }
    if test:
        r = requests.get(test_url, headers=test_headers)
        return r

    files = {'file': (os.path.basename(filename), open(filename, 'rb'), 'application/octet-stream')}
    pin_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    pin_header = {
        'pinata_api_key': env_config["IPFS_API_Key"],
        'pinata_secret_api_key': env_config["IPFS_API_Secret"],
    }
    r = requests.post(pin_url, files=files, headers=pin_header)
    return r