/** Some basic JS for all pages on jsutlovic.com */

$(function(){
  /* 
   * Use jQuery jScrollPane script for scrolling "scrollable" content:
   * Shift the vertical gutter (where the scroller appears) 8 pixels left,
   * and refresh when the browser resizes
   */
  $('div.main.container.scroll section article.scrollable').each(
  function() {
    $(this).jScrollPane(
      {
        verticalGutter: -8,
      }
    );
    var api = $(this).data('jsp');
    var throttleTimeout;
    $(window).bind(
      'resize',
      function()
      {
        if ($.browser.msie) {
          // IE fires multiple resize events while you are dragging the browser window which
          // causes it to crash if you try to update the scrollpane on every one. So we need
          // to throttle it to fire a maximum of once every 50 milliseconds...
          if (!throttleTimeout) {
            throttleTimeout = setTimeout(
              function()
              {
                api.reinitialise();
                throttleTimeout = null;
              },
              50
            );
          }
        } else {
          api.reinitialise();
        }
      }
    );
  });


 /*
  * Set all fancybox image links as a single gallery if
  * they don't have one already
  */
  $(".fancybox").each(function(index, elem){
    if (! $(elem).attr('rel')){
      $(elem).attr('rel', 'gallery')
    }
  });
  
  /*
   * Fancybox init:
   * Use buttons, at the bottom with the title outside the image
   * modal box, only use previous, next, scale and close buttons
   * Don't allow mouseWheel (gets annoying trying to scroll images)
   */
  $(".fancybox").fancybox({
    prevEffect    : 'none',
    nextEffect    : 'none',
    closeBtn    : false,
    mouseWheel  : false,
    helpers   : {
      title : { type : 'float' },
      buttons : {
        position: 'bottom',
        tpl: '<div id="fancybox-buttons"><ul><li><a class="btnPrev" title="Previous" href="javascript:;"></a></li><li><a class="btnNext" title="Next" href="javascript:;"></a></li><li><a class="btnToggle" title="Toggle size" href="javascript:;"></a></li><li><a class="btnClose" title="Close" href="javascript:jQuery.fancybox.close();"></a></li></ul></div>'},
    }
  });
});