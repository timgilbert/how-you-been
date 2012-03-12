/*
 * how-you-been.js
 * 
 * Routines for generating playlist data and whatnot
 */

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

function parseInspiration(inspirationList) {
  for (var i = 0; i < inspirationList.length; i++) {
    var data = inspirationList[i]; 
    var entry$ = $('#templates #entry').clone();
    entry$.data({'inspiration': data});
    $('#item', entry$).text(pickInspiration(data));
    $('#playlist').append(entry$);
  }
}