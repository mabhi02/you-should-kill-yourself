import pandas as pd
import numpy as np
import sys
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

restaurant_names = [] 
ratings = []

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
        rating = restaurant.get("rating", "Not rated")
        restaurant_names.append(name)
        ratings.append(rating)

if __name__ == "__main__":
    main()

print(restaurant_names)


#eat out
eatOut = 5 #Get this value from the form
specifications = "Mexican" #Get value from the form



# Step 2: Generate random values for positive and negative votes but will come from the platform
positive_votes = np.random.randint(0, 100, size=len(restaurant_names))
negative_votes = np.random.randint(0, 100, size=len(restaurant_names))

# Step 3: Determine local source or not based on the condition
local_source = positive_votes > negative_votes

# Step 4: Create the DataFrame
data = {
    "Restaurant": restaurant_names,
    "Rating": ratings,
    "Local Source Positive Votes": positive_votes,
    "Local Source Negative Votes": negative_votes,
    "Local Source or Not": local_source
}

df = pd.DataFrame(data)

local_df = df[df["Local Source or Not"] == True]

# Sort by "Rating" in descending order
sorted_local_df = local_df.sort_values(by="Rating", ascending=False)

# Get the top 'eatOut' rows
top_eatOut_df = sorted_local_df.head(eatOut)

print("Here is where you should eat out")
print(top_eatOut_df.head())
sys.stdout.flush()



