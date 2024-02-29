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
def create_page_properties(title, url, og_title=None, og_image=None, og_tags=None):
    properties = {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": og_title if og_title else "Content"
                    }
                }
            ]
        },
        "URL": {
            "url": url
        }
    }

    # Add cover image if available
    if og_image:
        properties["Files & media"] = {
            "files": [
                {
                    "name": "Image",
                    "type": "external",
                    "external": {
                        "url": str(og_image)  
                    }
                }
            ]
        }

    if og_tags:
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in og_tags]
        }

    return properties

# Create a new page in the specified database for the URL
async def create_pages_for_url(scraped_metadata, urls):
    try:
        for url, metadata in zip(urls, scraped_metadata):
            # Check if scraped_metadata is None
            if metadata is None:
                print("Error: No metadata scraped for the URL:", url)
                # Create a default title and set metadata to None
                og_title = "Content"
                og_description = None
                og_image = None
                og_tags = None
            else:
                # Extract metadata fields
                og_title = metadata.get('title')
                og_image = metadata.get('image')
                og_description = metadata.get('description')
                og_tags = metadata.get('tags')

            # Create page properties with the extracted metadata
            properties = create_page_properties(og_title, url, og_title, og_image, og_tags)

            # Create the Notion page
            page = client.pages.create(parent={"database_id": parent_database_id}, properties=properties, cover={"type": "external", "external": {"url": og_image}} if og_image else None)
            print("Page created for URL:", url)

            # Add child blocks to the page if metadata is available
            if og_description:
                client.blocks.children.append(
                    block_id=page["id"],
                    children=[
                        {
                            "object": "block",
                            "type": "heading_2",
                            "heading_2": {
                                "rich_text": [{"type": "text", "text": {"content": og_title}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"type": "text", "text": {"content": og_description}}]
                            }
                        }
                    ]
                )
    except Exception as e:
        print("Error creating page:", e)