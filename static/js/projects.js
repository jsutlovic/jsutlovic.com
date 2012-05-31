/* Projects-specific script */

//Shorten projects descriptions based on a span.readmore
$(function(){
  //Hide the extra text
  $(".readmore").hide();
  //append the readmore link to the end of the description text
  $(".readmore").parent().append("<span class='readmoreshow'>... <a href='#'>more</a></span>");
  //Hide the readmore link and show the text when the link is clicked
  $(".readmoreshow a").click(function() { 
    var _t = $(this); 
    _t.parent().hide();
    _t.parent().prev(".readmore").fadeIn('slow');    
  });
});
