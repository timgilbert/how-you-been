/**
 * The purpose of this file is to develop a weighted probability list.
 * Every element of the list has an associated weight; if x has weight 
 * 1 and y has weight 2, y is twice as likely as x to be selected at random. 
 */
function WeightedList(initial) { 
  this.weights = {};
  this.values = {};
  this.length = 0;
  
  if (initial != null) {
    for (var i = 0; i < initial.length; i++) {
      this.addItem(initial[i]);
    }
  }
}
WeightedList.prototype = {
  /**
   * Add an item to the list
   */
  addItem: function(weight, key, value) {
    this.values[key] = value;
    this.weights[key] = weight;
    this.length++;
  },
  
  /** 
   * Add the given weight to the list item with the given key
   */
  addWeight: function(key, weight) {
    this.weights[key] += weight;
  },
  
  /**
   * Select n random elements (without replacement), default 1.
   * If andRemove is true (default false), remove the elements
   * from the list.  (This is what the pop() method does.)
   */
  peek: function(n, andRemove) {
    if (n == null) {
      n = 1;
    }
    andRemove = !!andRemove;
    
    heap = this._buildWeightedHeap();
    result = [];
    
    for (var i = 0; i < n; i++) {
      key = head.pop();
      result.push({key: key, value: this.values[key]});
      if (andRemove) {
        delete this.weights[key];
        delete this.values[key];
        this.length--;
      }
    }
    return result;
  },
  
  /**
   * Return the entire list in a random order
   */
  shuffle: function() {
    return this.peek(this.length);
  },
  
  /**
   * 
   */
  pop: function(n) {
    return peek(n, true);
  },
  
  /**
   * Build a WeightedHeap instance based on the data we've got
   */
  _buildWeightedHeap: function() {
    var items = [];
    for (var key in this.weights) {
      // skip over Object.prototype monkey-patching per
      // http://bonsaiden.github.com/JavaScript-Garden/#object.forinloop
      if (this.weights.hasOwnProperty(key)) {
        items.push([this.weights[key], key]);
      }
    }
    return new _WeightedHeap(items);
  }
}

/**
 * This is a javascript implementation of the algorithm described by 
 * Jason Orendorff here: http://stackoverflow.com/a/2149533/87990
 */
function _HeapNode(weight, value, total) {
  this.weight = weight;
  this.name = name;
  this.total = total;  // Total weight of this node and its children
}
/**
 * Note, we're using a heap structure here for its tree properties, not as a 
 * classic binary heap. A node heap[i] has children at heap[i<<1] and at 
 * heap[(i<<1)+1]. Its parent is at h[i>>1]. Heap[0] is vacant.
 */
function _WeightedHeap(items) {
  this.heap = [null];   // Math is easier to read if we index array from 1
  
  // First put everything on the heap 
  for (var i = 0; i < items.length; i++) {
    var weight = items[i][0];
    var value = items[i][1];
    this.heap.append(new _HeapNode(weight, value, weight))
  }
  // Now go through the heap and each node's weight to its parent
  for (i = this.heap.length - 1; i >= 1; i--) {
    this.heap[i>>1].total += this.heap[i].total;
  }
}

_WeightedHeap.prototype = {
  pop: function() {
    // Start with a random amount of gas
    var gas = this.heap[1].total * Math.random();
    
    // Start driving at the root node
    var i = 1;  
    
    // While we have enough gas to keep going past i:
    while (gas > this.heap[i].weight) {
      gas -= this.heap[i].weight;     // Drive past i
      i <<= 1;                        // Move to first child
      if (gas > this.heap[i].total) {
        gas -= this.heap[i].total     // Drive past first child and its descendants
        i++;                          // Move on to second child
      }
    }
    // Out of gas - i is our selected node.
    var value = this.heap[i].value;
    var selectedWeight = this.heap[i].weight;
    
    this.heap[i].weight = 0;          // Make sure i isn't chosen again
    while (i > 0) {
      // Remove the weight from its parent's total
      this.heap[i].total -= selectedWeight
      i >>= 1;  // Move to the next parent
    }
    return value;
  }
};

//  NB: another binary heap implementation is at
// http://eloquentjavascript.net/appendix2.html
