import pandas as pd
import datetime
from datetime import datetime
import openai
import requests
import numpy as np
import sys
import requests
import argparse


def get_grocery_stores(api_key, location, radius=16093):  # 16093 meters ~ 10 miles
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    params = {
        "location": location,
        "radius": radius,
        "type": "grocery_or_supermarket",
        "key": api_key
    }
    
    grocery_stores = []
    
    while True:
        response = requests.get(base_url, params=params)
        result = response.json()
        
        if response.status_code != 200:
            print(f"Error: {result.get('error_message', 'Unknown error')}")
            return grocery_stores
        
        grocery_stores.extend(result.get("results", []))
        
        next_page_token = result.get("next_page_token")
        if not next_page_token:
            break
        
        params["pagetoken"] = next_page_token
        import time
        time.sleep(2)  # Wait for 2 seconds before making the next request
    
    return grocery_stores

grocery_store_names = [] 
ratings = []

def main():
    parser = argparse.ArgumentParser(description="Find grocery stores using Google Places API")
    parser.add_argument("api_key", help="Google Maps API Key")
    parser.add_argument("location", help="Latitude and longitude (e.g., 37.7749,-122.4194)")
    args = parser.parse_args()
    
    grocery_stores = get_grocery_stores(args.api_key, args.location)
    
    print(f"\nFound {len(grocery_stores)} grocery stores:")
    for i, store in enumerate(grocery_stores, 1):
        name = store.get("name", "Unknown")
        rating = store.get("rating", "Not rated")
        grocery_store_names.append(name)
        ratings.append(rating)
        print(f"{i}. {name} (Rating: {rating})")

if __name__ == "__main__":
    main()

print(grocery_store_names)

call = "python eatIn.py AIzaSyDoCCNgmaUfYf526pxNbzALKswaThqMByc 37.7749,-122.4194"




# Initialize OpenAI API key (replace 'your-api-key' with the actual API key)
openai.api_key = "sk-proj-h1x4dXFxCD5IDy1TcoWTT3BlbkFJjLvf3m8P25Msp7mHYycG"

# Sample fridge data GET FROM FORM as {Item, Quantity, Expiration_Date}
fridge_data = [
    {"item": "Chicken Breast", "quantity": 2, "expiration_date": "2024-07-05"},
    {"item": "Bell Pepper", "quantity": 3, "expiration_date": "2024-07-02"},
    {"item": "Onion", "quantity": 5, "expiration_date": "2024-07-10"},
    {"item": "Tomato", "quantity": 4, "expiration_date": "2024-07-03"},
    {"item": "Lettuce", "quantity": 1, "expiration_date": "2024-07-04"},
    {"item": "Cheese", "quantity": 2, "expiration_date": "2024-07-08"},
    {"item": "Tortilla", "quantity": 10, "expiration_date": "2024-07-01"},
    {"item": "Beef", "quantity": 1, "expiration_date": "2024-07-05"},
    {"item": "Rice", "quantity": 2, "expiration_date": "2024-08-01"},
    {"item": "Beans", "quantity": 3, "expiration_date": "2024-09-01"}
]

# Define the number of meals per day and week
meals_per_day = 3
days_per_week = 7
meals_outside = 4
total_meals = meals_per_day * days_per_week - 4

# Define a function to check expiration dates
def is_expired(expiration_date):
    today = datetime.now().date()
    exp_date = datetime.strptime(expiration_date, "%Y-%m-%d").date()
    return today > exp_date


# Filter out expired items
fridge = [item for item in fridge_data if not is_expired(item["expiration_date"])]

# Convert fridge data to a formatted string
def fridge_to_string(fridge):
    return ", ".join([f"{item['quantity']} {item['item']}" for item in fridge])

# Create a prompt to get meal suggestions
def create_meal_plan(fridge):
    prompt = f"I have the following items in my fridge: {fridge_to_string(fridge)}. I am also eating out {meals_outside} times a week so include an 'OUTSIDE' that many times. Please create a 7-day meal plan with 3 meals a day (breakfast, lunch, dinner). If there are not enough ingredients for a meal, indicate what additional ingredients are needed. Quantify how many ingredients you use and will need to buy. "
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message["content"]

# Generate the meal plan
meal_plan = create_meal_plan(fridge)

# Print the meal plan
print("Meal Plan for the Week:")
print(meal_plan)