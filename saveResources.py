import csv
from notion.client import NotionClient

csv_file_path = 'D:/Python Projects/Second-Brain-Bot/resources/urls.csv'

# Read URLs from the CSV file
def read_urls_from_csv(csv_file_path):
    urls = []
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            urls.extend(row)
    return urls

# Create cards in Notion for each URL
def create_cards_in_notion(urls):
    # Connect to Notion
    client = NotionClient(token_v2="secret_KErVYRcqQ9yhh372WS4tklt9sCUDzuxKd9LH8jQvPVB")
    # Load your Notion page
    page = client.get_block("18f688770e37421b8510b9c58072aee6")

    # Create a card for each URL
    for url in urls:
        # Create a new card in your Notion page
        new_card = page.children.add_new("link_to_page", title=url)
        new_card.set("link", url)

if __name__ == "__main__":
    # Read URLs from the CSV file
    csv_file_path = 'D:/Python Projects/Second-Brain-Bot/resources/urls.csv'
    urls = read_urls_from_csv(csv_file_path)

    # Create cards in Notion for each URL
    create_cards_in_notion(urls)