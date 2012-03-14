/*
 * how-you-been.js
 * 
 * Routines for generating playlist data and whatnot
 */


function initPlaylistPage() {
  generatePlaylist();
}

function initHomePage() {
  if ($.cookie('foursquare.oauth')) {
    $('#foursquareLogin').hide();
    $('#foursquareLoggedInMessage').show();
  }
  if ($.cookie('lastfm.sessionKey')) {
    console.debug('Yikes');
    $('#lastfmLogin').hide();
    $('#lastfmLoggedInMessage').show();
  }
}

function generatePlaylist() {
  var oauth = $.cookie('foursquare.oauth');

  if (oauth == null) {
    // If there's no cokie, redirect to home page
    window.location = '/';
  }

  $.getJSON(
      '/inspiration.json', 
      {'oauth': oauth}, 
      parseInspiration
  );
}
/**
 * Given one of the inspiration objects returned from /inspiration.json,
 * pick a random field.
 * 
 * I'm tempted to make the percentage distribution configurable at the server level, 
 * but this will suffice for now 
 */
function pickInspiration(inspiration) {
  // Generate a random number from 0-99
  var pick = Math.floor(Math.random() * 100);
  var key = '';
  
  if (pick <= 65) {
    key = 'venueName';
  }
  else if (pick <= 75) {
    key = 'categoryName';
  }
  else if (pick <= 85) {
    key = 'street';
  }
  else if (pick <= 90) {
    if (inspiration.crossStreet != null) {
      key = 'crossStreet';
    } else {
      key = 'street';
    }
  }
  else if (pick <= 95) {
    key = 'city';
  }
  else if (pick <= 98) {
    key = 'state';
  }
  else {
    key = 'country';
  }
  
  return inspiration[key];
}

// Ah, javascript, you never cease to amaze me with your elegance
// This is from http://stackoverflow.com/a/1404100/87990
function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) || [,null]) [1]
    );
}

/** First pass at searching: synchronous */


/**
 * Clone a single copy of the track div, attach data to it, and return it
 */
function createTrack(data, index) {
  var entry$ = $('#templates #track').clone();
  entry$.data({'inspiration': data, 'index': index});

  var inspiration = pickInspiration(data);
  $('.inspiration', entry$).text(inspiration);
  $('button.search', entry$).click(function(event) {
    searchForTrack(inspiration, entry$);
  });
  //console.log(index + ": " + inspiration)
  return entry$;
}

/**
 * 
 */
function searchForTrack(term, entry$) {
  var lastfm = new LastFM({'apiKey': lastFmApiKey});
  lastfm.track.search({'track': term}, {
    'success': function(data) {
      var hits = data.results['opensearch:totalResults'];
      if (hits <= 0) {
        $('.artist', entry$).text('???').show();
        // We should look for another source of inspiration here
        return;
      }
      $('.artist', entry$).text(hits + ' tracks found').show();
      console.info(data);
    },
    'error': function(code, message) {
      console.error('lastfm error ' + code + ': ' + message);
    }
  });
  console.info('search:' + term);
}

/**
 * After a successful Ajax call, go through the resulting list and populate 
 * the initial playlist.
 */
function parseInspiration(inspirationList) {
  for (var i = 0; i < inspirationList.length; i++) {
    var data = inspirationList[i]; 
    $('#playlist').append(createTrack(inspirationList[i], i));
  }
}
