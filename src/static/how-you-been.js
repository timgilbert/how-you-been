/*
 * how-you-been.js
 * 
 * Routines for generating playlist data and whatnot
 */

/*
 * Startup script - this sets up actions that will be run as soon as the page is loaded.
 */
$(function() {
  $('button#go').click(function(event) {
    var oauth = getURLParameter('oauth');
    console.debug('oauth:' + oauth);
    $('#playlist').empty();
    // Grab the JSON data
    $.getJSON('/inspiration.json', {'oauth': oauth}, parseInspiration);
  });
});


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

  //console.log(index + ": " + inspiration)
  return entry$;
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
