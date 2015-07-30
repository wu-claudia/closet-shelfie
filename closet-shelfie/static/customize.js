$(document).ready(function(){

  $("#top").hover(function(){
    $(this).animate(
      {opacity:0.5},
    10
    );
  });


  // $("#color").change(function() {
  //     var value = $(this).val();
  //     // var last3chars = value.substring(value.length - 3);
  // $("div[class]").hide();
  //     $('div[class='value']').show();
  // });

  $("button[name=delete]").click(function(){
    console.log($(this).val());
    $(this).parents(".item").fadeOut(
      1000
    );
    $.post( "/delete", { item: $(this).val()} );
  });


  // $("#color").change(function(e){
  //   $.map($('div.access.color'), function(e){$('.'+e.value).hide(); });
  //   $('.'+$('div.access.color').val()).show()
  //   });
  //   $("div#FilterContainer").find("div").hide();
  //   $("div#FilterContainer").find("div." + filters).show();
  // });
});
