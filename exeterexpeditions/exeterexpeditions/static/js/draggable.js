function initialiseDraggable(item, image, drag_container) {
  clue2_txt_top = ((98 - $("#clue2-txt").height()) / 2) + "px";
  $("#clue2-txt").css("top", clue2_txt_top);

  var dragItem = document.querySelector(item);
  var dragImage = document.querySelector(image);
  var container = document.querySelector(drag_container);

  var active = false;
  var currentX;
  var currentY;
  var initialX;
  var initialY;
  var xOffset = 0;
  var yOffset = 0;

  draggableAreaWidth = $(item + "-container").width();

  container.addEventListener("touchstart", dragStart, false);
  container.addEventListener("touchend", dragEnd, false);
  container.addEventListener("touchmove", drag, false);

  container.addEventListener("mousedown", dragStart, false);
  container.addEventListener("mouseup", dragEnd, false);
  container.addEventListener("mousemove", drag, false);

  function dragStart(e) {
    console.log("initialX: " + initialX + " currentX: " + currentX);
    if (e.type === "touchstart") {
      initialX = e.touches[0].clientX - xOffset;
      initialY = e.touches[0].clientY - yOffset;
    } else {
      initialX = e.clientX - xOffset;
      initialY = e.clientY - yOffset;
    }

    if (e.target === dragItem || e.target === dragImage) {
      active = true;
    }
  }

  function drag(e) {
    if (active) {
      sliderSnappingBack = true;

      e.preventDefault();

      if (e.type === "touchmove") {
        currentX = e.touches[0].clientX - initialX;
        currentY = e.touches[0].clientY - initialY;
      } else {
        currentX = e.clientX - initialX;
        currentY = e.clientY - initialY;
      }

      xOffset = currentX;
      yOffset = currentY;

      setClueBoxTextOpacity(dragItem);

      if(xOffset < 0) {

      } else if ((draggableAreaWidth - xOffset) > 97) {
        setTranslate(currentX, currentY, dragItem);
      } else {

      }

    }
  }

  function setTranslate(xPos, yPos, el) {
    el.style.transform = "translate3d(" + xPos + "px, " + 0 + "px, 0)";
  }

  function dragEnd(e) {

    active = false;
      sliderSnappingBack = false;

    if ((draggableAreaWidth - xOffset) <= 97) {
      clueNotBeingLoaded = false;
      document.getElementById(drag_container.slice(1)).innerHTML = '<div class="loader small"></div>';
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          response_json = JSON.parse(this.responseText);
          document.getElementById("clues-list").innerHTML = response_json['clue_list_content'];

          if(response_json['clue_level'] == 1) {

          } else if (response_json['clue_level'] == 2){
            initialiseDraggable("#clue2", "#clue2-img", "#clue2-container")
          }

          clueNotBeingLoaded = true;
        }
        };
        xhttp.open("GET", "/displayClueContent", true);
        xhttp.send();
      }
      };
      xhttp.open("GET", "/unlockClue", true);
      xhttp.send();

      initialX = 0;
      initialY = 0;

      xOffset = 0;
      yOffset = 0;
    } else {

      var id = setInterval(frame, 7);
      function frame() {
        if (xOffset <= 0) {
          clearInterval(id);
          xOffset = 0;
          sliderSnappingBack = false;
        } else {
          xOffset = xOffset - 5;
          setClueBoxTextOpacity(dragItem);
          setTranslate(xOffset, currentY, dragItem);
          }
        }
    }
  }

  function setClueBoxTextOpacity(element) {
    var textId = "";

    if(element.id == "clue1") {
      textId = "clue1-txt"
    } else if (element.id == "clue2") {
      textId = "clue2-txt"
    }

    textToChange = document.getElementById(textId);

    if((xOffset) > 115) {
      textToChange.style.filter = "opacity(0%)";
    } else {
      opacityValue = 115 - xOffset / 115 * 100;
      textToChange.style.filter = "opacity(" + opacityValue + "%)";
    }
  }
}
