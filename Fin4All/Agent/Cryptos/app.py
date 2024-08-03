import requests
import pandas as pd

def fetch_latest_news():
    url = "https://api.spaceflightnewsapi.net/v4/articles/"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "limit": 10,  # Fetch the latest 10 articles
        "order_by": "-published_at"  # Order by the latest published articles
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"News saved to {filename}")
    else:
        print("No data to save.")

def main():
    news = fetch_latest_news()
    
    if not news:
        print("No news articles found.")
        return
    
    # Filter relevant data for CSV
    filtered_news = []
    for article in news:
        filtered_news.append({
            "id": article.get("id"),
            "title": article.get("title"),
            "url": article.get("url"),
            "imageUrl": article.get("image_url"),
            "newsSite": article.get("news_site"),
            "summary": article.get("summary"),
            "publishedAt": article.get("published_at")
        })
    
    # Save news to CSV
    news_filename = "latest_news.csv"
    save_to_csv(filtered_news, news_filename)
    
    print(f"Latest news saved to {news_filename}")

if __name__ == '__main__':
    main()
