import requests
import json

def fetch_epic_offers():
    # الرابط الرسمي والصحيح لـ GraphQL
    url = "https://graphql.epicgames.com/graphql"
    
    # استعلام محسن لجلب العروض
    query = """
    query searchStoreQuery($country: String!, $locale: String!) {
      Catalog {
        searchStore(category: "games/edition/base", count: 100, country: $country, locale: $locale) {
          elements {
            title
            productSlug
            price(country: $country) {
              totalPrice {
                discountPrice
                originalPrice
                currencyCode
                fmtPrice {
                  discountPrice
                  originalPrice
                }
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "country": "EG",
        "locale": "ar"
    }
    
    # إضافة User-Agent لتجنب حظر الـ Actions (سبب الـ 404 غالباً)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("Connecting to Epic Games API...")
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            games = data['data']['Catalog']['searchStore']['elements']
            deals = []
            for game in games:
                price_info = game['price']['totalPrice']
                # نتحقق مما إذا كان هناك خصم فعلي
                if price_info['discountPrice'] < price_info['originalPrice']:
                    deals.append({
                        "title": game['title'],
                        "slug": game['productSlug'],
                        "original_price": price_info['fmtPrice']['originalPrice'],
                        "discount_price": price_info['fmtPrice']['discountPrice'],
                        "currency": price_info['currencyCode']
                    })
            
            with open('offers.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            print(f"Success! Created offers.json with {len(deals)} items.")
            
        except (KeyError, TypeError) as e:
            print(f"Error parsing data: {e}")
    else:
        print(f"Failed to fetch data. Status Code: {response.status_code}")
        # طباعة جزء من الاستجابة لمعرفة السبب
        print(response.text[:200])

if __name__ == "__main__":
    fetch_epic_offers()
