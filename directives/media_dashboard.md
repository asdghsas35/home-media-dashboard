# Media Dashboard Directive

## Goal
Run a local media dashboard that aggregates data from Plex, Qbittorrent, Sonarr, and Radarr.

## Inputs
- **Environment Variables** (in `.env`):
    - `PLEX_URL`, `PLEX_TOKEN`
    - `QBITTORRENT_URL`, `QBITTORRENT_USERNAME`, `QBITTORRENT_PASSWORD`
    - `SONARR_URL`, `SONARR_API_KEY`
    - `RADARR_URL`, `RADARR_API_KEY`

## Tools
- `execution/app.py`: The main Flask application.
- `execution/fetch_plex.py`: Fetches Plex data.
- `execution/fetch_qbittorrent.py`: Fetches Qbittorrent data.
- `execution/fetch_sonarr.py`: Fetches Sonarr data.
- `execution/fetch_radarr.py`: Fetches Radarr data.

## Instructions
1.  **Configure `.env`**: Ensure all API keys and URLs are correct.
2.  **Run the Dashboard**:
    ```bash
    # Activate virtual environment
    source .venv/bin/activate
    
    # Run the app
    python execution/app.py
    ```
3.  **Access the Dashboard**: Open your browser to `http://localhost:7152`.

## Troubleshooting
- **Connection Errors**: Check if the services (Plex, Sonarr, etc.) are running and accessible from this machine. Verify URLs in `.env`.
- **Authentication Errors**: Verify API keys and tokens in `.env`.
- **Missing Dependencies**: Ensure `flask` and `requests` are installed (`pip install flask requests`).

## How to Retrieve Tokens

### Plex Token (`PLEX_TOKEN`)
1.  Sign in to Plex.tv in your browser.
2.  Click on any media item (movie or episode).
3.  Click the three dots **(...)** menu > **Get Info**.
4.  Click **View XML**.
5.  A new tab will open with XML data. Look at the URL bar.
6.  The token is the string after `X-Plex-Token=`.
    - Example: `...&X-Plex-Token=abc123xyz...` -> Application Token is `abc123xyz`.

### Sonarr / Radarr API Key
1.  Open Sonarr or Radarr in your browser.
2.  Go to **Settings** > **General**.
3.  Scroll down to the **Security** section.
4.  Copy the **API Key**.

### Qbittorrent Credentials
- By default, the username is `admin` and the password is `adminadmin`.
- If you have changed these, use your custom credentials.
- Ensure "Bypass authentication for clients on localhost" is unchecked if you want to test authentication, or check it if you want to skip auth (but the script uses auth).


