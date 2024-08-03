import requests

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

def main():
    top_stocks = fetch_top_stocks()
    for stock in top_stocks:
        print(stock)

if __name__ == '__main__':
    main()
