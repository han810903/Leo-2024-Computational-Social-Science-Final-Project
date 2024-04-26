#Full script for scraping Duolingo user reviews from Google Play and Apple Store
import csv
from google_play_scraper import reviews_all, Sort
from app_store_scraper import AppStore

def scrape_google_play_reviews(app_id, num_reviews=1000):
    try:
        # Scrape reviews from Google Play
        reviews = reviews_all(
            app_id,
            sleep_milliseconds=1000,  # Sets a delay between requests
            sort=Sort.NEWEST,         # Sort by newest reviews
            count=num_reviews         # Number of reviews to scrape
        )
        return [{'content': review['content'], 'score': review['score']} for review in reviews]
    except Exception as e:
        print(f"Error scraping Google Play: {e}")
        return []

def scrape_app_store_reviews(app_name, num_reviews=1000):
    try:
        # Initialize the scraper for the specific app
        scraper = AppStore(country="us", app_name=app_name, app_id=570060128)
        # Retrieve a specified number of reviews
        scraper.review(how_many=num_reviews)
        return [{'content': review['review'], 'score': review['rating']} for review in scraper.reviews]
    except Exception as e:
        print(f"Error scraping Apple Store: {e}")
        return []

def save_reviews_to_csv(reviews, filename):
    # Save reviews to a CSV file
    headers = ['content', 'score']
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for review in reviews:
            writer.writerow(review)

def main():
    google_app_id = 'com.duolingo'  # Google Play ID for Duolingo
    apple_app_name = 'duolingo'  # Apple App Store name for Duolingo

    # Define the number of reviews to fetch
    num_reviews = 1000

    # Fetch and save Google Play reviews
    google_reviews = scrape_google_play_reviews(google_app_id, num_reviews)
    if google_reviews:
        save_reviews_to_csv(google_reviews, 'duolingo_reviews_google.csv')
        print(f"Saved {len(google_reviews)} Google Play reviews to 'duolingo_reviews_google.csv'")
    else:
        print("No reviews were scraped from Google Play.")

    # Fetch and save Apple App Store reviews
    apple_reviews = scrape_app_store_reviews(apple_app_name, num_reviews)
    if apple_reviews:
        save_reviews_to_csv(apple_reviews, 'duolingo_reviews_apple.csv')
        print(f"Saved {len(apple_reviews)} Apple App Store reviews to 'duolingo_reviews_apple.csv'")
    else:
        print("No reviews were scraped from the Apple App Store.")

if __name__ == "__main__":
    main()