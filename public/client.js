// client-side js
// run by the browser each time your view template is loaded

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function() {
  console.log('hello world :o');
  
  function getExcuses() {
    $.get('/excuses', function(excuse) {
      $('#excuse').fadeOut(function() {
        $(this).text(excuse)
      }).fadeIn();
    })
  };

  $('#new-excuse').click(getExcuses);

});

