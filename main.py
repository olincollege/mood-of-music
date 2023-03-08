"""
Functions to determine the overall "mood" of a user's Spotify Wrapped playlist
"""
import numpy
import spotipy
import validators
import credit

TEST_URL = "https://open.spotify.com/playlist/1XbedDdXpoV8Q0YUQpoyDQ"

client_credentials_manager = spotipy.SpotifyClientCredentials(
    client_id=credit.SPOTIPY_CLIENT_ID, client_secret=credit.SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def playlist_uri(link):
    """
    Return the Spotify URI from an input URL

    Args:
        link: A string representing the URL of a user's playlist

    Returns:
        A string representing the URI of a user's playlist
    """
    try:
        if validators.url(link):
            uri = link.split("/")[-1].split("?")[0]
            return uri
        return print("Please enter a valid link. Try again")
    except TypeError:
        return print("Please enter a valid link. Try again")


def get_track_id(link):
    """
    Return a list of Spotify Track IDs from an input URL

    Args:
        link: A string representing the URL of a user's playlist

    Returns:
        A list representing all the track IDs of a user's playlist
    """
    track_uri = playlist_uri(link)
    track_id = [x["track"]["id"] for x in sp.playlist_tracks(track_uri)["items"]]
    return track_id


def get_valence(link):
    """
    Return a list of "valence" values for each track in a user's playlust

    Valence refer to a measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.
    Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric),
    while tracks print(happy_meter(TEST_URL))

        A list of integers representing all the valence values from a user's playlist
    """
    track_id = get_track_id(link)
    valence = []
    for ids in track_id:
        valence.append(sp.audio_features(ids)[0]["valence"])
    return valence


def average_valence(link):
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
    all_valence = get_valence(link)
    return numpy.mean(all_valence)


def how_happy(link):
    """
    Return a message telling how happy a user was that year
    based on a user's Spotify Wrapped playlist

    Args:
        link: A string representing the URL of a user's playlist

    Returns:
        A string that is message of how happy a user was
    """
    happiness_meter = numpy.round(average_valence(link), decimals=2)
    year = input("Enter when this playlist was made: ")
    return print(f"You were about {happiness_meter} happy out of 1 in {year}!")


how_happy(input("Enter your Spotify Playlist Link: "))
