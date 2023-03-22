"""
Functions to determine the overall "mood" of a user's Spotify Wrapped playlist
"""
import numpy
import spotipy
import validators
import google_spreadsheet
import spotify_key

TEST_URL = "https://open.spotify.com/playlist/1XbedDdXpoV8Q0YUQpoyDQ"

client_credentials_manager = spotipy.SpotifyClientCredentials(
    client_id=spotify_key.SPOTIPY_CLIENT_ID,
    client_secret=spotify_key.SPOTIPY_CLIENT_SECRET,
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def playlist_uri(playlist_link):
    """
    Return the Spotify URI from an input URL

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A string representing the URI of a user's playlist
    """
    try:
        if validators.url(playlist_link):
            uri = playlist_link.split("/")[-1].split("?")[0]
            return uri
    except spotipy.exceptions.SpotifyException:
        return print("Please enter a valid link. Try again")


def get_track_id(playlist_link):
    """
    Return a list of Spotify Track IDs from an input URL

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A list representing all the track IDs of a user's playlist
    """
    track_uri = playlist_uri(playlist_link)
    track_id = [x["track"]["id"] for x in sp.playlist_tracks(track_uri)["items"]]
    return track_id


def get_username(playlist_link):
    """
    Return the name of the owner of a playlist

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A string representing the name of the owner

    """
    name = sp.playlist_items(playlist_link)["items"][0]["added_by"]["id"]
    name = name.capitalize()
    return name


def get_valence(playlist_link):
    """
    Return a list of "valence" values for each track in a user's playlust

    Valence refer to a measure from 0.0 to 1.0 describing
    the musical positiveness conveyed by a trac.itemse URL of a user's playlist

    Returns:
        A list of integers representing all the valence values from a user's playlist
    """
    track_id = get_track_id(playlist_link)
    valence = []
    for ids in track_id:
        valence.append(sp.audio_features(ids)[0]["valence"])
    return valence


def average_valence(playlist_link):
    """
    Return an integer that represents how happy a user was
    Based on a user's Spotify Wrapped playlist

    Function will return an average "valence" value from
    all the valence values from a user's playlist

    Args:
        link: A string representing the URL of a user's playlist

    Returns:
        An integer representing the average valence of a playlist
    """
    all_valence = get_valence(playlist_link)
    return numpy.mean(all_valence)


def culmative_valence():
    """
    Return the culmative valence for the year of the playlists

    Returns:
        A dictionary for each of the culmative valences from the Year 2019 to 2022
    """
    spreadsheet_data = google_spreadsheet.googlesheet()

    for year, playlists in spreadsheet_data.items():
        playlists = [average_valence(link) for link in playlists]
        spreadsheet_data[year] = numpy.round(numpy.mean(playlists), decimals=2)

    return spreadsheet_data


def how_happy_is(playlist_link):
    """
    Return a message telling how happy a user was that year
    based on a user's Spotify Wrapped playlist

    This function is for users who individually requested their
    playlist results to be reported back

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A string that is a message of how happy a user was
    """
    happiness_meter = numpy.round(average_valence(playlist_link), decimals=2)
    name = get_username(playlist_link)
    year = input("Enter when this playlist was made: ")
    return print(
        f"{name} was about {happiness_meter} happy out of 1 in the Year {year}!"
    )


culmative_valence()
