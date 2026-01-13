import requests
import json

def fetch_epic_offers():
    # هذا الرابط مخصص للعروض والترقيات في متجر إيبيك
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    
    params = {
        "locale": "ar",
        "country": "EG",
        "allowCountries": "EG"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("Connecting to Epic Games Deals API...")
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        try:
            # الوصول إلى قائمة الألعاب
            elements = data['data']['Catalog']['searchStore']['elements']
            deals = []
            
            for game in elements:
                price_info = game.get('price', {}).get('totalPrice', {})
                
                # نتحقق من وجود تخفيض (السعر الحالي أقل من الأصلي)
                discount_price = price_info.get('discountPrice', 0)
                original_price = price_info.get('originalPrice', 0)
                
                if discount_price < original_price:
                    deals.append({
                        "title": game.get('title'),
                        "id": game.get('id'),
                        "description": game.get('description'),
                        "original_price_fmt": price_info.get('fmtPrice', {}).get('originalPrice'),
                        "discount_price_fmt": price_info.get('fmtPrice', {}).get('discountPrice'),
                        "currency": price_info.get('currencyCode'),
                        "expiry_date": None # يمكن استخراجه من الـ promotions إذا لزم الأمر
                    })

            # حفظ النتائج
            with open('offers.json', 'w', encoding='utf-8') as f:
                json.dump(deals, f, ensure_ascii=False, indent=4)
            
            print(f"Success! Created offers.json with {len(deals)} items.")
            
        except KeyError as e:
            print(f"Error structure changed: {e}")
    else:
        print(f"Failed again. Status Code: {response.status_code}")
        print("Reason:", response.reason)

if __name__ == "__main__":
    fetch_epic_offers()
