/**
 * The purpose of this file is to develop a weighted probability list.
 * Every element of the list has an associated weight; if x has weight 
 * 1 and y has weight 2, y is twice as likely as x to be selected at random. 
 */
function WeightedList() { 
  //this.items = []
  this.names = {}
  this.totalWeight = 0
  this.heap = new BinaryHeap(function(item) {
    return item[0];
  });
}
WeightedList.prototype = {
  addItem: function(weight, name, data) {
    this.heap.push([weight, name]);
    this.names[name] = data
    this.totalWeight += weight
  },
  
  addScore: function(name, score) {
    
  },
  
  // pick with replacement
  // Algorithm from here: http://stackoverflow.com/a/2149533/87990
  pick: function(n) {
    if (n == null) {
      n = 1
    }
    var result = [];
    var i = 0;
    var total = this.totalWeight;
    var w = this.items[0][0];
    var v = this.items[0][1];
    while (n > 0) {
      var x = total * (Math.pow(1 - Math.random(), 1.0 / n));
      total -= x;
      while (x > w) {
        x -= w;
        i++;
        w = this.items[i][0];
        v = this.items[i][1];
      }
      w -= x;
      result.push({name: v, data: this.names[v]});
      n--;
    }
    return result;
  }
  
  // pick without replacement involves a binary heap, see:
  // http://eloquentjavascript.net/appendix2.html
  pick_without_replacement: function(n) {
    
  }
}

/**
 * This is a javascript implementation of the algorithm described by 
 * Jason Orendorff here: http://stackoverflow.com/a/2149533/87990
 */
function _HeapNode(weight, value, total) {
  this.weight = weight;
  this.name = name;
  this.total = total;
}
/**
 * Note, we're using a heap structure here for its tree properties, not as a 
 * classic binary heap. A node heap[i] has children at heap[i<<1] and at 
 * heap[(i<<1)+1]. Its parent is at h[i>>1]. Heap[0] is vacant.
 */
function WeightedHeap(items) {
  this.heap = [null];   // Math works out better if we index array from 1
  
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

WeightedHeap.prototype = {
  popRandom: function() {
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
