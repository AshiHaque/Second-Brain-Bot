import os
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

# Define properties for the new page
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

# Create a new page in the specified database with the properties
page = client.pages.create(parent={"database_id": parent_database_id}, properties=properties,  cover= {"type": "external","external": {"url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"}})
