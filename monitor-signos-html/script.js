(function worker() {
  $.ajax({
    url: 'http://127.0.0.1:3000/temperatura', 
    success: function(data) {
      $('#temp').html(data);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 500);
    }
   });
 })();
