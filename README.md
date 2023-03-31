# Mood Of Music
As the range of the variety of music grows over time, research has shown how an individual's music preferences correlate to their mood. To fully utilize this correlation, our project aims to call from the Spotify API to analyze a user's overall mood for a year, specfically the year 2020: the start of the COVID-19 Pandemic. 
</br>
</br>
At the end of every year, Spotify provides the user a playlist called "Spotify Wrapped", which consists of the user's top songs from the past year. The Spotify API also provides audio features for each track, such as "danceability","liveness","speechiness",etc. Among these features, our team uses the "valence" metric, which represents the musical postiviness conveyed by a track. 
</br>
</br>
According to Spotify, "Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sounds more negative (e.g. sad, depressed, angry). Therefore, through analyzing the valence values across a user's "Spotify Wrapped" from years 2019 to 2022, our project will observe whether a significant change of happiness is apparent during the periods before and after COVID-19.
</br>
</br>

## Required Software
To run the software, you will need the following:
* numpy
* pandas
* matplotlib
* spotipy
* google_spreadsheet
* requests
* validators
* google-api-python-client 
* google-auth-httplib2
* google-auth-oauthlib
* (To use the Spotify API) Spotify Web API Access Token
* (To access the spreadsheet) Google OAuth 2.0 Token

</br>

### Library Installation
* To install all of the necessary libraries, make sure you're running a version of Python that is 3.7 or above
* Ensure that your file directory is at the root of the repository. Then, look for a file called `requirements.txt`. Afterwards, run the following:
```
pip install -r requirements.txt
```
* Now you have all the libraries to run our code!

</br>

### Spotify Web API
To access the Spotify Web API, you will need an Access Token:
* [Please follow the instructions here](https://developer.spotify.com/documentation/web-api)

Once you have your token, create a file called `spotify_key.py` and enter your details into the following format:
```
SPOTIPY_CLIENT_ID = "abcdefghijklmop"

SPOTIPY_CLIENT_SECRET = "12345678956789"

SPOTIPY_REDIRECT_URI = "http://localhost/"
```
Save this file in the root of the repository and you should be set. MAKE SURE NOT TO SHARE THIS WITH ANYONE 

</br>

### Google OAuth 2.0 Token
Since "Spotify Wrapped" Playlists are private playlists, our project sent out a survey for people to share their playlists into a public format.
</br>
</br>
These results are written on to a Google Sheets spreadsheet, which our code directly calls data from.


To access the Google Spreadsheet, you will need a Google OAuth 2.0 Token:
* [Please follow the instructions here](https://developers.google.com/identity/protocols/oauth2)

* Go to [API & Service](https://console.cloud.google.com/apis) in the Google Cloud Platform

* Go to [Credentials](https://console.cloud.google.com/apis/credentials) and click "Create Credentials" for an OAuth client ID (Web Application)

* Once you have your token visit [Credentials](https://console.cloud.google.com/apis/credentials) again and download the OAuth 2.0 Client `json` file, then save this file as 'google_token.json' in the root of the repository. MAKE SURE NOT TO SHARE THIS WITH ANYONE 

* Enable the [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com) and the [Gmail API](https://console.cloud.google.com/apis/library/gmail.googleapis.com) on the API Library Menu

* Finally, contact Chang Jun Park (cpark1@olin.edu), Swasti Jain (sjain1@olin.edu), or Allan Huang (ahuang2@olin.edu) to request access to the spreadsheet

* Please make sure to include details for why you would need this data. 

That should be all. You're all set!
</br>
</br>
If you have any other questions, please contact one of the people above.

### Bonus
We've included a special function called `email_results.py`, which sends the valence results of their playlists to those who submitted their email on the survey. Please do not run this function! We have already emailed the results of the survey . We only ask you to appreciate the beauty of the code :). 
