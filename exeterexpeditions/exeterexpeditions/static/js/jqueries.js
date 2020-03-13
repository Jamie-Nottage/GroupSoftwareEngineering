videoWidth = 0;
pageWidth = 0;

$(document).ready(function(){

  $(".faq-question").click(function(elem) {
      if($(this).next().css("display") == "none") {
        $(this).next().css("display", "block");
      } else {
        $(this).next().css("display", "none");
      }

    });

    $("#map-container").load("static/htmlcontent/map.html");
});
