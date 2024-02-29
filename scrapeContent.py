import requests
from bs4 import BeautifulSoup
from tiktokapipy.api import TikTokAPI

def scrape_open_graph_metadata(url):
    try:
        if 'tiktok.com' in url:  # Check if the URL is a TikTok video URL
            # Initialize TikTok API
            with TikTokAPI() as api:
                video = api.video(url)

                # Extract metadata from the TikTok video
                og_author = video.author
                og_image = video.image_post
                og_description = video.desc

                # Print the extracted metadata
                print("TikTok Video Metadata:")
                print("Author:", og_author)
                print("Image:", og_image)
                print("Description:", og_description)
                
                return og_author, og_image, og_description
        
        else:
            # Send a GET request to the URL
            response = requests.get(url)
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
                
                return og_title, og_image, og_description, og_tags
            else:
                print("Failed to fetch the URL:", response.status_code)
                return None, None, None, None
    except Exception as e:
        print("Error:", e)
        return None, None, None, None

if __name__ == "__main__":
    # Set the URL for testing (TikTok video URL)
    url = 'https://www.youtube.com/watch?v=6WXMivVkiR8&ab_channel=CoffeeShopVibes'
    
    # Call the function with the test URL
    og_title, og_image, og_description, og_tags = scrape_open_graph_metadata(url)