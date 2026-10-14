import os
import pandas as pd
import requests


class Genius:
    # Initialize the Genius class with the API access token
    def __init__(self, access_token):
        self.access_token = access_token

    def get_artist(self, search_term):
        # Step 1: Set up the authorization header
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        # Step 2: Search for the artist
        search_url = "https://api.genius.com/search"

        response = requests.get(
            search_url,
            headers=headers,
            params={"q": search_term},
            timeout=15
        )
        response.raise_for_status()

        # Convert the search response into a dictionary
        search_data = response.json()
        hits = search_data.get("response", {}).get("hits", [])

        # Return an empty dictionary if no results are found
        if not hits:
            return {}

        # Step 3: Get the primary artist ID from the first search result
        first_hit = hits[0]
        artist_id = first_hit["result"]["primary_artist"]["id"]

        # Return an empty dictionary if no matching artist is found
        if artist_id is None:
            return {}

        # Step 4: Retrieve detailed information about the artist
        artist_url = f"https://api.genius.com/artists/{artist_id}"

        artist_response = requests.get(
            artist_url,
            headers=headers,
            timeout=15
        )
        artist_response.raise_for_status()

        # Convert the artist response into a dictionary
        artist_data = artist_response.json()

        # Return the artist information if available
        return artist_data

    def get_artists(self, search_terms):
        # Create a list to store information about multiple artists
        artists = []

        # Search for each artist in the provided list
        for term in search_terms:
            artist = self.get_artist(term)["response"]["artist"]

            # Store the required details for each search term
            artists.append({
                "search_term": term,
                "artist_name": artist.get("name"),
                "artist_id": artist.get("id"),
                "followers_count": artist.get("followers_count")
            })

        # Convert the collected artist details into a DataFrame
        return pd.DataFrame(artists)
