$(document).ready(function(){

  $("#top").hover(function(){
    $(this).animate(
      {opacity:0.5},
    10
    );
  });


  $(function(){
  $("#color").bind("change", function() {
      var value = $(this).find("option:selected").val();
      // var last3chars = value.substring(value.length - 3);
  $("div[class]").hide();
      $(".class_" + value).show();
  });
  });

  // $("#color").change(function(e){
  //   $.map($('div.access.color'), function(e){$('.'+e.value).hide(); });
  //   $('.'+$('div.access.color').val()).show()
  //   });
  //   $("div#FilterContainer").find("div").hide();
  //   $("div#FilterContainer").find("div." + filters).show();
  // });
});
