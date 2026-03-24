#!/usr/bin/env python3
"""
Test script to verify itinerary generation
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, DEFAULT_TEMPERATURE, DEFAULT_MAX_OUTPUT_TOKENS

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": DEFAULT_TEMPERATURE,
        "max_output_tokens": DEFAULT_MAX_OUTPUT_TOKENS
    }
)

# Test parameters
travel_params = {
    'destination': 'Paris',
    'days': '3',
    'people': '2',
    'accommodation': 'mid-range',
    'activities': 'sightseeing',
    'interests': 'culture, food',
    'budget': 'medium'
}

# Simple prompt
prompt = f"""
Create a detailed {travel_params['days']}-day travel itinerary for {travel_params['destination']} in markdown format.

# {travel_params['destination']} - {travel_params['days']} Day Travel Plan

## Day-by-Day Itinerary

IMPORTANT: Create a detailed itinerary for EACH of the {travel_params['days']} days.

### Day 1: [Theme]
**Morning (8:00 AM - 12:00 PM)**
- Activity 1: [Specific location]
- Activity 2: [Another location]

**Afternoon (12:00 PM - 6:00 PM)**
- Lunch: [Restaurant]
- Activity 3: [Location]

**Evening (6:00 PM - 10:00 PM)**
- Dinner: [Restaurant]
- Evening activity: [Location]

[REPEAT FOR ALL {travel_params['days']} DAYS]

## Budget Breakdown
- Total estimated cost

CRITICAL: You MUST create a complete day-by-day itinerary for all {travel_params['days']} days.
"""

print("Testing itinerary generation...")
print("=" * 60)

try:
    response = model.generate_content(prompt)
    result = response.text
    
    print(f"Response length: {len(result)} characters")
    print("=" * 60)
    
    # Check if itinerary sections exist
    has_day_1 = "Day 1" in result
    has_day_2 = "Day 2" in result
    has_day_3 = "Day 3" in result
    has_morning = "Morning" in result
    has_afternoon = "Afternoon" in result
    has_evening = "Evening" in result
    
    print(f"✓ Has Day 1: {has_day_1}")
    print(f"✓ Has Day 2: {has_day_2}")
    print(f"✓ Has Day 3: {has_day_3}")
    print(f"✓ Has Morning section: {has_morning}")
    print(f"✓ Has Afternoon section: {has_afternoon}")
    print(f"✓ Has Evening section: {has_evening}")
    print("=" * 60)
    
    if all([has_day_1, has_day_2, has_day_3, has_morning, has_afternoon, has_evening]):
        print("✅ SUCCESS: Itinerary generated correctly!")
    else:
        print("❌ ISSUE: Some itinerary sections are missing")
    
    print("\nFirst 500 characters of response:")
    print(result[:500])
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
