import requests
import argparse

def get_restaurants(api_key, location, cuisine, radius=16093):  # 16093 meters ~ 10 miles
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": location,
        "radius": radius,
        "type": "restaurant",
        "keyword": cuisine,
        "key": api_key
    }
    
    restaurants = []
    
    while True:
        response = requests.get(base_url, params=params)
        result = response.json()
        
        if response.status_code != 200:
            print(f"Error: {result.get('error_message', 'Unknown error')}")
            return restaurants
        
        restaurants.extend(result.get("results", []))
        
        next_page_token = result.get("next_page_token")
        if not next_page_token:
            break
        
        params["pagetoken"] = next_page_token
        import time
        time.sleep(2)  # Wait for 2 seconds before making the next request
    
    return restaurants

def main():
    parser = argparse.ArgumentParser(description="Find restaurants using Google Places API")
    parser.add_argument("api_key", help="Google Maps API Key")
    parser.add_argument("location", help="Latitude and longitude (e.g., 37.7749,-122.4194)")
    parser.add_argument("cuisine", help="Cuisine type")
    args = parser.parse_args()
    
    restaurants = get_restaurants(args.api_key, args.location, args.cuisine)
    
    print(f"\nFound {len(restaurants)} restaurants:")
    for i, restaurant in enumerate(restaurants, 1):
        name = restaurant.get("name", "Unknown")
        address = restaurant.get("vicinity", "Address not available")
        rating = restaurant.get("rating", "Not rated")
        print(f"{i}. {name}")
        print(f"   Address: {address}")
        print(f"   Rating: {rating}")
        print()

if __name__ == "__main__":
    main()