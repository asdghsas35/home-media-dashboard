import urllib.request
import json
import os
from dotenv import load_dotenv

load_dotenv()

def debug_overseerr():
    base_url = os.getenv('OVERSEERR_URL')
    api_key = os.getenv('OVERSEERR_API_KEY')
    
    if not base_url or not api_key:
        print("Error: Overseerr not configured in .env")
        return

    base_url = base_url.rstrip('/')
    headers = {
        'X-Api-Key': api_key,
        'Accept': 'application/json'
    }
    
    print(f"Connecting to {base_url}...")
    
    try:
        url = f"{base_url}/api/v1/request?take=5&sort=added&skip=0"
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        print(f"Total results: {data.get('pageInfo', {}).get('results')}")
        
        results = data.get('results', [])
        if not results:
            print("No requests found.")
            return

        print("\n--- First Request Item Structure ---")
        first_item = results[0]
        print(json.dumps(first_item, indent=2))
        
        print("\n--- Analysis ---")
        media = first_item.get('media', {})
        print(f"Media Object Keys: {list(media.keys())}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_overseerr()
