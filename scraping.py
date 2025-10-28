import requests
import re
from bs4 import BeautifulSoup

# Function to scrape specific data from the website
def fetch_web_data(url):
    """
    Fetches data from the given URL and extracts its title, meta description,
    headings, hyperlinks, navigation menu, images, news, and contact info.
    """
    try:
        # Send a request to the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the page title
        title = soup.title.string.strip() if soup.title else "No title found"

        # Extract the meta description
        meta_desc = soup.find("meta", {"name": "description"})
        description = meta_desc["content"].strip() if meta_desc else "No meta description found"

        # Extract main headings (H1 and H2)
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]
        h2_tags = [h2.get_text(strip=True) for h2 in soup.find_all("h2")]

        # Extract hyperlinks
        links = [a["href"] for a in soup.find_all("a", href=True)]
        links = [link for link in links if link.startswith("http")]

        # Extract navigation menu
        nav_items = [item.get_text(strip=True) for item in soup.select("nav a")]
        nav_menu = nav_items if nav_items else ["No navigation menu found"]

        # Extract images
        images = [
            {"src": img.get("src", "").strip(), "alt": img.get("alt", "No alt text").strip()}
            for img in soup.find_all("img")
            if img.get("src")
        ]

        # Extract news or articles
        news_items = []
        for article in soup.select(".teaser"):  # Adjust selector based on the site's HTML structure
            headline = article.get_text(strip=True)
            link = article.find("a")["href"] if article.find("a") else "No link available"
            if headline:
                # Convert relative links to absolute URLs
                full_link = requests.compat.urljoin(url, link)
                news_items.append({"headline": headline, "link": full_link})

        # Extract contact information
        email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        phone_regex = r"\+?[0-9]{1,3}[-.\s]?[0-9]{2,4}[-.\s]?[0-9]{4,10}"

        emails = set(re.findall(email_regex, soup.text))
        valid_emails = [email.strip() for email in emails if email]

        phone_numbers = set(re.findall(phone_regex, soup.text))
        valid_phone_numbers = [phone.strip() for phone in phone_numbers if len(phone.strip()) >= 7]

        # Format and return the results
        result = (
            f"Title: {title}\n"
            f"Description: {description}\n\n"
            f"News:\n" + (
                "\n".join([f"Headline: {item['headline']}, Link: {item['link']}" for item in news_items])
                if news_items
                else "No news items found"
            ) + "\n\n"
            f"Contact Info:\n"
            f"  Emails: {', '.join(valid_emails) if valid_emails else 'No emails found'}\n"
            f"  Phone Numbers: {', '.join(valid_phone_numbers) if valid_phone_numbers else 'No phone numbers found'}\n"
        )
        return result.strip()
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {str(e)}"

# Integrate web scraping into chatbot
def handle_user_input_with_scraping(user_input, question_and_answers=None):
    """
    Handles user input and triggers scraping if the input starts with 'scrape'.
    """
    if user_input.startswith("scrape "):  # Example command: scrape <URL>
        url = user_input.split(" ", 1)[-1].strip()
        result = fetch_web_data(url)
        print(result)
    else:
        print("Handle other chatbot functionality here.")

# Example usage for the given URL
if __name__ == "__main__":
    # Example user input for testing
    example_input = "scrape https://www.tagesschau.de/"
    handle_user_input_with_scraping(example_input)