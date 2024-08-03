import requests

def fetch_top_crypto(filter='all-crypto', top_n=50):
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
    print("\nTop Trending Cryptocurrencies on Reddit in the past 24 hours:")
    top_cryptos = fetch_top_crypto()
    for crypto in top_cryptos:
        print(crypto)

if __name__ == '__main__':
    main()
