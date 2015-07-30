$(document).ready(function(){
  $(".combo button[name=delete]").click(function(){
    console.log($(this).val());
    $(this).parents(".combo").fadeOut(
      1000
    );
    $.post( "/delete", { combo: $(this).val()} );
  });

});
