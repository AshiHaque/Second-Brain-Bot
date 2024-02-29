import asyncio
import requests
from bs4 import BeautifulSoup
from tiktokapipy.async_api import AsyncTikTokAPI

async def scrape_open_graph_metadata(url):
    try:
        if 'tiktok.com' in url:  # Check if the URL is a TikTok video URL
            # Initialize TikTok API asynchronously
            async with AsyncTikTokAPI() as api:
                video = await api.video(url)

                # Extract metadata from the TikTok video
                og_author = video.author
                og_image = video.image_post
                og_description = video.desc

                # Print the extracted metadata
                print("TikTok Video Metadata:")
                print("Author:", og_author)
                print("Image:", og_image)
                print("Description:", og_description)

                # Return the metadata in a consistent format
                return {
                    'title': og_author,
                    'image': og_image,
                    'description': og_description,
                    'tags': None  # TikTok videos have tags in the description
                }

        else:
            # Send a GET request to the URL asynchronously
            response = await asyncio.get_event_loop().run_in_executor(None, lambda: requests.get(url))
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find Open Graph meta tags
                og_title_tag = soup.find("meta", property="og:title")
                og_image_tag = soup.find("meta", property="og:image")
                og_description_tag = soup.find("meta", property="og:description")
                og_tags_tag = soup.find("meta", property="og:tags")

                # Check if tags exist before accessing their content
                og_title = og_title_tag['content'] if og_title_tag else None
                og_image = og_image_tag['content'] if og_image_tag else None
                og_description = og_description_tag['content'] if og_description_tag else None
                og_tags = og_tags_tag['content'] if og_tags_tag else None

                # Print the extracted metadata
                print("Open Graph Metadata:")
                print("Title:", og_title)
                print("Image:", og_image)
                print("Description:", og_description)
                print("Tags:", og_tags)

                # Return the metadata in a consistent format
                return {
                    'title': og_title,
                    'image': og_image,
                    'description': og_description,
                    'tags': og_tags
                }
            else:
                print("Failed to fetch the URL:", response.status_code)
                return None
    except Exception as e:
        print("Error:", e)
        return None
