import requests
import os
from bs4 import BeautifulSoup
import sys
import re
import urllib.parse

# Create output directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Base URL
base_url = "https://oldschool.runescape.wiki"

# Read ogg_urls.txt and iterate over each line
with open('ogg_urls.txt', 'r') as file:
    for line in file:
        # Extract the part of the link
        part_of_link = line.strip().replace('/w/File:', '')

        # Construct the output file name
        encoded_output_filename = os.path.join("output", os.path.basename(part_of_link))
        output_filename = urllib.parse.unquote(encoded_output_filename)

        # Check if the file already exists in the output folder
        if os.path.exists(output_filename):
            print(f"File {output_filename} already exists. Skipping download.")
            continue

        # Append part_of_link to the base URL
        full_url = f"{base_url}/w/File:{part_of_link}"

        try:
            # Send a GET request to the URL
            response = requests.get(full_url) 

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the content to find the download link
                soup = BeautifulSoup(response.content, 'html.parser')
                download_link_tag = soup.find('a', href=re.compile("\/images\/(.+)\.ogg")) 
                # Check if download_link_tag is None or empty
                if not download_link_tag or not download_link_tag.get('href'):
                    print(f"No download link found for {full_url}")
                    print(download_link_tag)
                    sys.exit()  # Stop the entire script

                  
                if download_link_tag:
                    # Extract the actual download URL
                    download_url = base_url + download_link_tag.get('href')

                    # Download the .ogg file
                    ogg_file = requests.get(download_url)

                    # Save the .ogg file locally
                    encoded_file_name = os.path.basename(download_url)
                    file_name = urllib.parse.unquote(encoded_file_name).split('.ogg')[0] + '.ogg'
                    with open(os.path.join(output_dir, file_name), 'wb') as output_file:
                        output_file.write(ogg_file.content)
                    print(f"Downloaded {file_name}")
                else:
                    print(f"No download link found for {full_url}")

            else:
                print(f"Failed to download {full_url}. Status code: {response.status_code}")

        except Exception as e:
            print(f"Error downloading {full_url}: {str(e)}")

