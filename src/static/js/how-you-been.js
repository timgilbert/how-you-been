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
 * After a successful Ajax call, go through the resulting list and populate 
 * the initial playlist.
 */
function parseInspiration(inspirationList) {
  for (var i = 0; i < inspirationList.length; i++) {
    var inspirationStore = new InspirationStore(inspirationList[i]);
    $('#playlist').append(createTrack(inspirationStore, i));
  }
}

/**
 * Clone a single copy of the track div, attach data to it, and return it
 */
function createTrack(inspirationStore, index) {
  var entry$ = $('#templates #track').clone();
  
  //entry$.data({'inspiration': inspirationStore, 'index': index});
  $('.inspiration', entry$).text(inspirationStore.activeInspiration.value);
  
  // When we get a call back from last.fm, this handler will be called
  entry$.bind('lastFmReady', function(event, trackStore) {
    console.debug('lastFmReady', trackStore);
    $('.inspiration', this).text(inspirationStore.activeInspiration.value);
    if (trackStore.hits <= 0) {
      // No hits found
      $('.notfound', this).show();
      return;
    }
    $('.found', this).show();
    $('.tracksFound', this).text(trackStore.hits);
    
    var track = trackStore.best();
    //console.debug(track);
    $('.artist', this).text(track.artist);
    $('.name', this).text(track.name);
    $('.name', this).attr('href', track.url);
    if (track.image) {
      $('.thumbnail', this).attr('src', track.image);
    }
    $('button.search', this).removeAttr('disabled');
  });
  
  // Button handler.  If this is successful, a 'lastFmReady' event will be fired 
  // (see handler above)
  $('button.search', entry$).click(function(event) {
    $('button.search', this).attr('disabled', true);
    inspirationStore.searchForTrack(entry$);
  });
  
  //console.log(index + ": " + inspiration)
  return entry$;
}

/**
 * Main interface to the inspiration list returned by the server.  Each track 
 * will have one of these attached.  Most tracks will only use the first one, 
 * but in case there are no hits on the first inspiration, we'll drop back to 
 * the next chosen one.
 * 
 */
function InspirationStore(inspiration) {
  // TODO: could probably generalize this out a bit more
  var inspirationWeights = {
    venueName: 50,
    eventName: 50,
    categoryName: 25,
    street: 10,
    crossStreet: 10,
    city: 5,
    state: 2,
    country: 1
  };
  var weightedList = new WeightedList();
  for (field in inspiration) {
    if (inspiration.hasOwnProperty(field)) {
      weightedList.push(field, inspirationWeights[field], inspiration[field]);
    }
  }
  this.unusedInspirations = weightedList.shuffle();
  this.usedInspirations = [];
  this.getNextInspiration();
  
  this.lastfm = new LastFM({'apiKey': lastFmApiKey});
}

InspirationStore.prototype = {
  /** Go to the next possible inspiration */
  getNextInspiration: function() {
    this.usedInspirations.push(this.activeInspiration);
    this.activeInspiration = this.unusedInspirations.shift();
    return this.activeInspiration;
  },
  
  /** 
   * Search the inspiration lists until we find one that returns some results;
   * return those results
   * 
   * TODO: should definitely use jquery custom events or similar for this
   */
  searchForTrack: function(entry$) {
    var result = null;
    var inspirationStoreInstance = this;
    
    this.lastfm.track.search({'track': this.activeInspiration.value}, {
      'success': function(data) {
        trackStore = new TrackStore(data);
        console.debug('trackStore:', trackStore);
        entry$.trigger('lastFmReady', trackStore);
      },
      'error': function(code, message) {
        console.error('lastfm error ' + code + ': ' + message);
        return null;
      }
    });
    
    return result;
  }
}

function TrackStore(data) {
  this.hits = data.results['opensearch:totalResults'];
  if (this.hits <= 0) {
    return;
  }
  
  //console.debug('d', data);
  //console.debug('dr', data.results);
  //console.debug('drt', data.results.trackmatches);
  var matches = data.results.trackmatches.track;
  if (matches == null) {
    console.error('Unable to find data.results.trackmatches.track in', data)
  }
  this. trackList = new WeightedList();
  
  for (var i = 0; i < matches.length; i++) {
    var track = new Track(matches[i]);
    var weight = track.weight();
    
    // TBD: prefer artists this user likes (via last.fm/tasteometer)
    // TBD (maybe) prefer globally popular tracks? via track.listeners
    this.trackList.push(track.key, weight, track);
  }
   
  //this.data = data;
}
TrackStore.prototype = {
  /**
   * Return the best track (eg, pop the next item from the weighted list)
   */
  best: function() {
    return this.trackList.pop(1, true);
  }
}

/** 
 * This is (shallow) facade around last.fm/track.Search's results.trackMatches.track[i]
 */ 
function Track(matchData) {
  this.artist = matchData.artist;
  this.name = matchData.name;
  this.url = matchData.url;
  this.listeners = matchData.listeners;
  
  this.streamable = matchData.streamable['#text'] == '1';
  this.fullTrack = this.streamable && matchData.streamable['fulltrack'] == '1';
  
  if (typeof(matchData.image) !== 'undefined') {
    for (var i = 0; i < matchData.image.length; i++) {
      if (matchData.image[i].size == 'large') {
        this.image = matchData.image[i]['#text'];
        //console.debug('image', this.image, matchData.image[i]);
      }
    }
  }
  
  // Good enough for a hash-table key, though we could theoretically get collisions
  this.key = this.artist + ' ** ' + this.name;
}

Track.prototype = {
  /** Return a basic weight for this track */
  weight: function() {
    var result = 10;
    
    // Prefer streamable tracks
    if (this.streamable) {
      result *= 10;
    }
    // Prefer full tracks
    if (this.fulltrack) {
      result *= 5;
    }
    // Prefer tracks with images
    if (this.image) {
      result *= 10; 
    }
    
    return result;
  }
}

// Ah, javascript, you never cease to amaze me with your elegance
// This is from http://stackoverflow.com/a/1404100/87990
function getURLParameter(name) {
    return decodeURI(
        (RegExp(name + '=' + '(.+?)(&|$)').exec(location.search) || [,null]) [1]
    );
}

/** First pass at searching: synchronous */



