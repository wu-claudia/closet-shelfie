$(document).ready(function(){

  $(my_outfit).click(function(){
    $(.my_outfit).fadeout();
  });

  $("#top").mouseover(function(){
    $(this).animate(
      {opacity:0.5},
    10
    );
});
