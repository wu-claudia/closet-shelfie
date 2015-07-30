$(document).ready(function(){

  $(my_outfit).click(function(){
    $(.my_outfit).fadeout();
  });

  $("select.filterby").change(function(){
    var filters = $.map($("select.filterby").toArray(),function(e){
      return $(e).val();
    }).join(".");
    $("div#FilterContainer").find("div").hide();
    $("div#FilterContainer").find("div." + filters).show();
  });
});
