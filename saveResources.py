import os
import csv
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables from .env file
load_dotenv()

# Retrieve the integration token from the environment variable
integration_token = os.getenv("NOTION_INTEGRATION_TOKEN")

# Initialize Notion client with the integration token
client = Client(auth=integration_token)

# Specify parent database ID
parent_database_id = "af58ab4dbc1c4d68ad71b66d1d284732"

# Read URLs from the CSV file
csv_file_path = 'D:/Python Projects/Second-Brain-Bot/resources/urls.csv'
def read_urls_from_csv(csv_file_path):
    urls = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.extend(row)
    return urls

# Define properties for the new page
def create_page_properties(url):
    properties = {
    "Name": {
        "title": [
            {
                "text": {
                    "content": "Test"
                }
            }
        ]
    },
    "Tags": {
        "multi_select": [
            {"name": "Tag1"},
            {"name": "Tag2"}
        ]
    },
    "Files & media": {
        "files": [
            {
                "name": "File Name",
                "type": "external",
                "external": {
                    "url": "https://example.com/file"
                }
            }
        ]
    },
    "URL": {
        "url": "https://example.com"
    }
}
    return properties

# Create a new page in the specified database for each URL
def create_pages_for_urls(urls):
    for url in urls:
        properties = create_page_properties(url)
        page = client.pages.create(parent={"database_id": parent_database_id}, properties=properties,  cover= {"type": "external","external": {"url": "https://images.unsplash.com/photo-1488190211105-8b0e65b80b4e?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzkyMXwwfDF8c2VhcmNofDV8fGNvbnRlbnR8ZW58MHx8fHwxNzA5MDk4MTc3fDA&ixlib=rb-4.0.3&q=80&w=200"}})
        print("Page created for URL:", url)

if __name__ == "__main__":
    # Read URLs from the CSV file
    urls = read_urls_from_csv(csv_file_path)

    # Create pages in Notion for each URL
    create_pages_for_urls(urls)