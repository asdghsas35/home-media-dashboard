import urllib.request
import urllib.error
import urllib.parse
import json
import os
import traceback

def fetch_plex_data():
    plex_url = os.getenv('PLEX_URL')
    plex_token = os.getenv('PLEX_TOKEN')
    
    if not plex_url or not plex_token:
        return {'error': 'Plex not configured'}

    plex_url = plex_url.rstrip('/')

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
        except urllib.error.HTTPError as e:
            return {'error': f'Plex HTTP Error {e.code}: Check PLEX_URL and PLEX_TOKEN'}
        except urllib.error.URLError as e:
            return {'error': f'Plex Connection Error: {e.reason} - Is PLEX_URL reachable from this machine?'}
        except json.JSONDecodeError:
            return {'error': 'Plex: Invalid JSON response. Check PLEX_URL.'}
        except Exception as e:
            return {'error': f'Plex: {str(e)}'}

    def get_latest_session():
        try:
            url = f"{plex_url}/status/sessions"
            req = urllib.request.Request(url, headers={'X-Plex-Token': plex_token, 'Accept': 'application/json'})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            if 'MediaContainer' in data and data['MediaContainer'].get('size', 0) > 0:
                sessions = []
                metadata = data['MediaContainer'].get('Metadata', [])
                for item in metadata:
                    user = item.get('User', {}).get('title', 'Unknown User')
                    user_thumb = item.get('User', {}).get('thumb')
                    if user_thumb:
                        user_thumb = f"{user_thumb}?X-Plex-Token={plex_token}" # It's usually a full URL but might need token if internal
                    
                    title = item.get('title')
                    # If episode
                    if item.get('type') == 'episode':
                        grandparent = item.get('grandparentTitle')
                        if grandparent:
                            title = f"{grandparent} - {title}"
                    
                    thumb = item.get('thumb')
                    if thumb:
                        thumb = f"{plex_url}{thumb}?X-Plex-Token={plex_token}"

                    sessions.append({
                        'user': user,
                        'user_thumb': user_thumb,
                        'title': title,
                        'thumb': thumb,
                        'year': item.get('year'),
                        'type': item.get('type')
                    })
                return sessions
            return []
        except urllib.error.URLError:
            return []
        except Exception:
            return []

    try:
        recent_movies = get_recent_items(1)
        # If movies fetch returned an error, bubble it up
        if isinstance(recent_movies, dict) and 'error' in recent_movies:
            return recent_movies

        recent_shows = get_recent_items(4)
        if isinstance(recent_shows, dict) and 'error' in recent_shows:
            return recent_shows

        active_sessions = get_latest_session()
        
        return {
            'movies': recent_movies,
            'shows': recent_shows,
            'active_sessions': active_sessions
        }
    except Exception as e:
        return {'error': str(e)}
