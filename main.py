"""
Functions to determine the overall "mood" of a user's Spotify Wrapped playlist
"""
import numpy
import spotipy
import google_spreadsheet
import spotify_key

# Load your Spotify API Credentials
client_credentials_manager = spotipy.SpotifyClientCredentials(
    client_id=spotify_key.SPOTIPY_CLIENT_ID,
    client_secret=spotify_key.SPOTIPY_CLIENT_SECRET,
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
RANGE_ALL = "B2:G"
RANGE_YEAR = "C2:F"


def playlist_uri(playlist_link):
    """
    Return the Spotify URI from an input URL

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A string representing the URI of a user's playlist
    """
    uri = playlist_link.split("/")[-1].split("?")[0]
    return uri


def get_track_id(playlist_link):
    """
    Return a list of Spotify Track IDs from an input URL

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A list representing the track IDs of a user's playlist
    """
    track_uri = playlist_uri(playlist_link)
    track_id = [
        x["track"]["id"]
        for x in sp.playlist_tracks(track_uri)["items"]
        if x is not None
    ]
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
    Return a list of "valence" values for each track in a user's playlist

    Valence refer to a measure from 0.0 to 1.0 describing
    the musical positiveness conveyed by a user's playlist

    Returns:
        A list of integers representing all the valence values from a user's playlist
    """
    track_id = get_track_id(playlist_link)
    valence = []
    for ids in track_id:
        valence_value = sp.audio_features(ids)
        if valence_value != [None]:
            valence.append(valence_value[0]["valence"])
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
    if playlist_link == "" or google_spreadsheet.link_testing(playlist_link) is False:
        return "'No Playlist Submitted'"
    all_valence = get_valence(playlist_link)
    return numpy.round(numpy.mean(all_valence), decimals=2)


def overall_valence():
    """
    Return the all and the overall average valence for the year of the playlists

    Returns:
        A dictionary for all of the average valences for each year
        A dictionary for each of the overall average valences
        from the Year 2019 to 2022
    """
    spreadsheet_data_all = google_spreadsheet.googlesheet_by_year()
    for year, playlists in spreadsheet_data_all.items():
        playlists = [average_valence(link) for link in playlists]
        spreadsheet_data_all[year] = playlists
    spreadsheet_average = {"2019": 0, "2020": 0, "2021": 0, "2022": 0}
    for year, averages in spreadsheet_data_all.items():
        spreadsheet_average[year] += numpy.round(numpy.mean(averages), decimals=2)
    return spreadsheet_data_all, spreadsheet_average


def valence_change():
    """
    Return the difference of valences for consecutive years

    Returns:
        A dictionary of keys'2019-2020','2020-2021','2021-2022'
        containing a list of valence differences for consecutive years
        across multiple users
    """
    change = {"2019-2020": [], "2020-2021": [], "2021-2022": []}
    spreadsheet_data = google_spreadsheet.googlesheet_difference()
    for valences in spreadsheet_data:
        valences = [average_valence(link) for link in valences]
        differences = numpy.round(numpy.diff(valences), decimals=2).tolist()
        change["2019-2020"].append(differences[0])
        change["2020-2021"].append(differences[1])
        change["2021-2022"].append(differences[2])
    return change


def how_happy_is(playlist_link):
    """
    Return a message telling how happy a user was that year
    based on a user's Spotify Wrapped playlist

    This function is for users who individually requested their
    playlist results to be reported back

    Args:
        playlist_link: A string representing the URL of a user's playlist

    Returns:
        A string that represents a message of how happy a user was for the year.
    """
    happiness_meter = numpy.round(average_valence(playlist_link))
    name = get_username(playlist_link)
    year = input("Enter when this playlist was made: ")
    return print(
        f"{name} was about {happiness_meter} happy out of 1 in the Year {year}!"
    )
