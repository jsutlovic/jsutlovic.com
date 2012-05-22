function switchHiMenu(mi) {
  $("nav.main.primary li.selected").removeClass("selected");
  mi.addClass("selected");
} 

function setHiMenuHash() {
  if(window.location.hash)
  {
    var whash = window.location.hash;
    switchHiMenu($("nav.main.primary a[href='" + whash + "']").parent('li'));
  }
}

function bindMenuClick(e) {
  var mi = $(this).parent('li');
  switchHiMenu(mi);
}

$(function(){
  setHiMenuHash();
  $("a#name").click(bindMenuClick);
  $("nav.main.primary a").click(bindMenuClick);
});
