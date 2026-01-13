import requests
import json

def fetch_epic_offers():
    url = "https://graphql.epicgames.com/graphql"
    
    # استعلام GraphQL لجلب العروض
    query = """
    {
      Catalog {
        searchStore(category: "games/edition/base", count: 10, country: "EG") {
          elements {
            title
            description
            productSlug
            price(country: "EG") {
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
            promotions(category: "games/edition/base") {
              promotionalOffers {
                promotionalOffers {
                  startDate
                  endDate
                  discountSetting {
                    discountPercentage
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json={'query': query}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        games = data['data']['Catalog']['searchStore']['elements']
        
        # تصفية الألعاب التي عليها خصم فقط
        deals = []
        for game in games:
            price_info = game['price']['totalPrice']
            if price_info['discountPrice'] < price_info['originalPrice']:
                deals.append({
                    "title": game['title'],
                    "slug": game['productSlug'],
                    "original_price": price_info['fmtPrice']['originalPrice'],
                    "discount_price": price_info['fmtPrice']['discountPrice'],
                    "currency": price_info['currencyCode']
                })
        
        # حفظ النتائج في ملف JSON
        with open('offers.json', 'w', encoding='utf-8') as f:
            json.dump(deals, f, ensure_ascii=False, indent=4)
        print(f"Done! Found {len(deals)} deals.")
    else:
        print(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_epic_offers()
