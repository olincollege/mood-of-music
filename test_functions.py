"""
Test library functions for Mood of Music Playlists.
"""
import google_spreadsheet

from main import playlist_uri, average_valence


def test_playlist_uri_regular():
    """
    Check a Spotify public playlist with a reguarlly formatted link.
    """
    url = "https://open.spotify.com/playlist/37i9dQZF1DWUa8ZRTfalHk"
    expected = "37i9dQZF1DWUa8ZRTfalHk"
    assert playlist_uri(url) == expected


def test_playlist_uri_question():
    """
    Check a Spotify public playlist link with a question mark in-between.
    """
    url = "https://open.spotify.com/playlist/29TRiiXCIQTT84JpR398jN?si=a3e5e6eec0fe4e52"
    expected = "29TRiiXCIQTT84JpR398jN"
    assert playlist_uri(url) == expected


def test_link_check_private():
    """
    Check whether the link is a Spotify public playlist.
    """
    url = "https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=fa8e755b4cbf419f&nd=1"
    expected = False
    assert google_spreadsheet.link_testing(url) == expected


def test_link_check_not_spotify():
    """
    Check whether the link is a Spotify link.
    """
    url = "https://google.com"
    expected = False
    assert google_spreadsheet.link_testing(url) == expected


def test_link_check_empty():
    """
    Check whether the link is empty.
    """
    url = ""
    expected = False
    assert google_spreadsheet.link_testing(url) == expected


def test_link_invalid():
    """
    Check whether the link is a valid link.
    """
    url = "Hi/dude?what"
    expected = False
    assert google_spreadsheet.link_testing(url) == expected


def test_average_valence_empty():
    """
    Check if error message is displayed with no playlist submitted.
    """
    url = ""
    expected = "'No Playlist Submitted'"
    assert average_valence(url) == expected


def test_average_valence_invalid():
    """
    Check if error message is displayed with invalid playlist link
    """
    url = "https://open.spotify.com/playlist/37i9dQZF1EUMDoJuT8yJsl?si=164c2f9bd9674fe3"
    expected = "'No Playlist Submitted'"
    assert average_valence(url) == expected
