import urllib.request
import urllib.error
import urllib.parse
import json
import os

def fetch_plex_data():
    plex_url = os.getenv('PLEX_URL')
    plex_token = os.getenv('PLEX_TOKEN')
    
    if not plex_url or not plex_token:
        return {'error': 'Plex not configured'}

    headers = {
        'Accept': 'application/json'
    }
    
    def get_recent_items(lib_type, limit=5):
        # type 1 = Movie, type 4 = Episode
        params = urllib.parse.urlencode({
            'type': lib_type,
            'sort': 'addedAt:desc',
            'limit': limit,
            'X-Plex-Token': plex_token
        })
        
        try:
            url = f"{plex_url}/library/all?{params}"
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            items = []
            if 'MediaContainer' in data and 'Metadata' in data['MediaContainer']:
                for item in data['MediaContainer']['Metadata']:
                    title = item.get('title')
                    if lib_type == 4: # Shows
                        grandparent = item.get('grandparentTitle', '')
                        parent = item.get('parentTitle', '') # Season
                        # Plex often puts show title in grandparentTitle for episodes
                        if grandparent:
                            title = f"{grandparent}" 
                        
                        items.append({
                            'title': title,
                            'episode': item.get('title'), # Episode name
                            'thumb': f"{plex_url}{item.get('thumb')}?X-Plex-Token={plex_token}" if item.get('thumb') else None
                        })
                    else:
                        items.append({
                            'title': title,
                            'year': item.get('year'),
                            'thumb': f"{plex_url}{item.get('thumb')}?X-Plex-Token={plex_token}" if item.get('thumb') else None
                        })
            return items
        except Exception as e:
            return [] # Fail silently for specific calls

    try:
        recent_movies = get_recent_items(1)
        recent_shows = get_recent_items(4)
        
        return {
            'movies': recent_movies,
            'shows': recent_shows
        }
    except Exception as e:
        return {'error': str(e)}
