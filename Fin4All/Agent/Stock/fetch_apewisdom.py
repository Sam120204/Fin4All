import requests
import json

def fetch_top_stocks(filter='all-stocks', top_n=50):
    base_url = 'https://apewisdom.io/api/v1.0/filter'
    page = 1
    results = []

    while len(results) < top_n:
        url = f"{base_url}/{filter}/page/{page}"
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            results.extend(data['results'])
            page += 1
        else:
            break

    return results[:top_n]

def save_to_json(data, filename='top_stocks.json'):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    print("Fetching Top Trending Stocks on Reddit...")
    top_stocks = fetch_top_stocks()
    save_to_json(top_stocks)
    print(f"Top trending stocks have been saved to 'top_stocks.json'.")

if __name__ == '__main__':
    main()