$(document).ready(function(){

  $("#top").hover(function(){
    $(this).animate(
      {opacity:0.5},
    10
    );
  });

  $("select.filterby").change(function(){
    var filters = $.map($("select.filterby").toArray(),function(e){
      return $(e).val();
    }).join(".");
    $("div#FilterContainer").find("div").hide();
    $("div#FilterContainer").find("div." + filters).show();
  });
});
