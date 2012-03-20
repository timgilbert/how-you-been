TODO
====

* The user should be able to select a particular week from a calendar picker and use 
that as the week range to get data from.

* Checkins for events should have those event names get high priority.

* Possible name change to haunting refrain?

* If we exhaust every possible search term for a track, there should be a placeholder,
which should probably be [4'33"][4-33].

* last.fm users should be able to optionally provide their usernames instead of logging 
all the way in, or opt-out of last.fm authentication entirely and just get a playlist

* Finish the last.fm playlist creation bit for logged-in users

* I should shamelessly rip off (with credit) the drag-and-drop Spotify creation method 
which [Spotibot][spotibot] uses.

* Better yet, I should be able to create a playlist in rdio, since they have a better 
API.

* We should look for badges earned during the week and bubble them up

Finished
--------

* Publish weighted list as its own library, with unit tests and the like
(it's up at [js-weighted-list][js-weighted-list])
* I may need to develop some sort of weighted-probability thing for javascript, since
I have several cases where I need to choose between several alternatives, I want to 
prefer some outcomes, and the complete set of possible outcomes is not know beforehand.

* In general, the server should perform last.fm and foursquare authentication and 
then pass those values to the front-end.  The front-end should store them in a 
session cookie.  User-facing URLs should display conditionally based on the existence 
of these cookies (I'm assuming no CDN caching for now).


Example record with event
-------------------------

    {u'comments': {u'count': 0, u'items': []},
     u'createdAt': 1329883654,
     u'event': {u'foreignIds': {u'count': 1, u'items': [{u'domain': u'songkick.com', u'id': 0}]},
                u'id': u'4ed84f237ed17c8b0570c82b',
                u'name': u'Frankie Rose, Dive and Night Manager'},
     u'id': u'4f446a06e4b0c38dc8499ee5',
     u'photos': {u'count': 0, u'items': []},
     u'source': {u'name': u'foursquare for Android', u'url': u'https://foursquare.com/download/#/android'},
     u'timeZone': u'America/New_York',
     u'type': u'checkin',
     u'venue': {u'categories': [{u'icon': {u'name': u'.png',
                                           u'prefix': u'https://foursquare.com/img/categories/arts_entertainment/musicvenue_rockclub_',
                                           u'sizes': [32, 44, 64, 88, 256]},
                                 u'id': u'4bf58dd8d48988d1e9931735',
                                 u'name': u'Rock Club',
                                 u'pluralName': u'Rock Clubs',
                                 u'primary': True,
                                 u'shortName': u'Rock Club'}],
                u'contact': {u'formattedPhone': u'(347) 529-6696',
                             u'phone': u'3475296696',
                             u'twitter': u'knittingfactory'},
                u'id': u'4aa6ccdaf964a520064b20e3',
                u'location': {u'address': u'361 Metropolitan Ave.',
                              u'city': u'Brooklyn',
                              u'country': u'United States',
                              u'crossStreet': u'at Havemeyer St.',
                              u'lat': 40.71431895905386,
                              u'lng': -73.95588642919986,
                              u'postalCode': u'11211',
                              u'state': u'NY'},
                u'name': u'The Knitting Factory',
                u'stats': {u'checkinsCount': 7411, u'tipCount': 63, u'usersCount': 5021},
                u'verified': False}},

[4-33]: http://www.last.fm/music/John+Cage/4%2733%27%27
[js-weighted-list]: https://github.com/timgilbert/js-weighted-list
[spotibot]: http://spotibot.com/playlist/
