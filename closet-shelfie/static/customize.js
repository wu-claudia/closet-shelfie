$(document).ready(function(){


  $("#color").change(function() {
      var value = $(this).val();
      // var last3chars = value.substring(value.length - 3);
      $("div[class]").hide();
      $(".item").each(function(i,elem){
        if ($(elem).hasClass(value)){
          $(elem).show();
        }
        else{
        }
      });
  });

  $(".item button[name=delete]").click(function(){
    console.log($(this).val());
    $(this).parents(".item").fadeOut(
      1000
    );
    $.post( "/delete", { item: $(this).val()} );
  });

});
