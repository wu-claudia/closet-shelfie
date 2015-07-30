$(document).ready(function(){

  $("#top").hover(function(){
    $(this).animate(
      {opacity:0.5},
    10
    );
  });

  $("#color").change(function(e){
    $.map($('div.access.color'), function(e){$('.'+e.value).hide(); });
    $('.'+$('div.access.color').val()).show()
    });
  //   $("div#FilterContainer").find("div").hide();
  //   $("div#FilterContainer").find("div." + filters).show();
  // });
});
