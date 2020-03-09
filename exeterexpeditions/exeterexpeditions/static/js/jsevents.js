var timedSignUpdate = setInterval(setSign, 3000);
var timedCluesUpdate = setInterval(updateClueContent, 3000);
var clueNotBeingLoaded = true;
var sliderSnappingBack = false;
var clue_image_source = "";

tn = "1";

function setSign() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    olddata = document.getElementById("movable-sign-txt").innerHTML;
    if(olddata != this.responseText){
      document.getElementById("movable-sign-txt").innerHTML = this.responseText;
      updateVisitedLocations(false);
    }
  }
  };
  xhttp.open("POST", "/getSign", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("teamname="+tn);
}

function setSignInitially() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("movable-sign-txt").innerHTML = this.responseText;

  }
  };
  xhttp.open("POST", "/getSign", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("teamname="+tn);
  updateVisitedLocations(true);
  updateClueContent();
}

function updateClueContent() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200 && clueNotBeingLoaded && !(sliderSnappingBack)) {
    response_json = JSON.parse(this.responseText);
    document.getElementById("clues-list").innerHTML = response_json['clue_list_content'];
    if(response_json['clue_level'] == 1) {
      initialiseDraggable("#clue1", "#clue1-img", "#clue1-container");
    } else if (response_json['clue_level'] == 2){
      initialiseDraggable("#clue2", "#clue2-img", "#clue2-container");
    }
    clue_image_source = response_json['clue_img'];
  }
  };
  xhttp.open("GET", "/displayClueContent", true);
  xhttp.send();
}

function updateVisitedLocations(initialUpdate) {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("central-list").innerHTML = this.responseText;
    if(initialUpdate && (this.responseText == "")) {
      showWelcomeScreen();
    }
  }
  };
  xhttp.open("POST", "/getCentralTable", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("teamname="+tn);
}

function showWelcomeScreen() {
  hideOverlay();
  showOverlay();
  document.getElementById("overlay-container").style.overflow = "scroll";
  document.getElementById("welcome-container").style.display = "block";
}

function checkIn() {
  if(document.getElementById("overlay-container").style.display == "block"){
    if(document.getElementById("checkin-button").style.backgroundColor == "orange") {
      hideOverlay();
      resetButtonColours();
    } else {
      hideOverlay();
      resetButtonColours();
      showQR();
      document.getElementById("checkin-button").style.backgroundColor = "orange";
    }
  } else {
    showQR();
  }

}

function leaderboard() {
  if(document.getElementById("overlay-container").style.display == "block"){
    if(document.getElementById("leaderboard-button").style.backgroundColor == "orange") {
      hideOverlay();
      resetButtonColours();
    } else {
      hideOverlay();
      resetButtonColours();
      showOverlay();
      document.getElementById("leaderboard-button").style.backgroundColor = "orange";
      loadLeaderboard();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("leaderboard-button").style.backgroundColor = "orange";
    loadLeaderboard();
  }
}

function loadLeaderboard(){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("leaderboard-container").innerHTML = this.responseText;
  }
  };
  xhttp.open("GET", "/getLeaderboard", true);
  xhttp.send();
  document.getElementById("leaderboard-container").style.display = "block";
  document.getElementById("overlay-container").style.overflow = "scroll";
  document.getElementById("overlay-container").style.backgroundColor = "#508CA4";
}

function map() {
  if(document.getElementById("overlay-container").style.display == "block"){
    if(document.getElementById("map-button").style.backgroundColor == "orange") {
      hideOverlay();
      resetButtonColours();
    } else {
      hideOverlay();
      resetButtonColours();
      showOverlay();
      document.getElementById("map-button").style.backgroundColor = "orange";
      loadMap();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("map-button").style.backgroundColor = "orange";
    loadMap();
  }
}

function loadMap() {
  document.getElementById("map-container").style.display = "block";
  document.getElementById("overlay-container").style.width = "95%";
  document.getElementById("overlay-container").style.borderWidth = "0.5vh";
  document.getElementById("overlay-container").style.left = "2.5%";

  $(function(){
      $("#map-container").load("static/htmlcontent/map.html");
    });
}

function achievements() {
  if(document.getElementById("overlay-container").style.display == "block"){
    if(document.getElementById("achievements-button").style.backgroundColor == "orange") {
      hideOverlay();
      resetButtonColours();
    } else {
      hideOverlay();
      resetButtonColours();
      showOverlay();
      document.getElementById("achievements-button").style.backgroundColor = "orange";
      loadAchievements();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("achievements-button").style.backgroundColor = "orange";
    loadAchievements();
  }
}

function loadAchievements() {
  document.getElementById("achievements-container").style.display = "block";
}

function chatbot() {
  if(document.getElementById("overlay-container").style.display == "block"){
    if(document.getElementById("chatbot-button").style.backgroundColor == "orange") {
      hideOverlay();
      resetButtonColours();
    } else {
      hideOverlay();
      resetButtonColours();
      showOverlay();
      document.getElementById("chatbot-button").style.backgroundColor = "orange";
      loadChatbot();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("chatbot-button").style.backgroundColor = "orange";
    loadChatbot();
    }
}

function loadChatbot() {
  document.getElementById("chatbot-container").style.display = "block";
  document.getElementById("overlay-container").style.overflow = "scroll";
}


function showQR() {
  document.getElementById("overlay-container").style.display = "block";
  document.getElementById("checkin-button").style.backgroundColor = "orange";
  document.getElementById("underlay-container").style.filter = "blur(10px)";
  document.getElementById("overlay-container").style.height = "1px";
  document.getElementById("overlay-container").style.width = "1px";
  document.getElementById("overlay-container").style.top = "25%";
  document.getElementById("overlay-container").style.overflow = "visible";
  document.getElementById("overlay-container").style.borderStyle = "none";
  document.getElementById("qr-scanner-container").style.display = "block";

  videoWidth = $(".qrPreviewVideo").width()
  pageWidth = $("#underlay-container").width()
  leftSpace = (pageWidth - videoWidth) / 2;
  $(".qrPreviewVideo").css("left", leftSpace);
}

function revealPhoto() {
  hideOverlay();
  resetButtonColours();
  showOverlay();
  document.getElementById("overlay-container").style.overflow = "scroll";
  document.getElementById("photo-container").style.display = "block";
  document.getElementById("overlay-container").style.width = "95%";
  document.getElementById("overlay-container").style.height = ($("#overlay-container").width()) * 0.75 + "px";
  document.getElementById("overlay-container").style.top = ((($(window).height()) - ($("#overlay-container").height())) / 3) + "px";
  document.getElementById("overlay-container").style.left = "2.5%";
  document.getElementById("photo-container").innerHTML = '<img id="photo-clue-img" src="'+ clue_image_source + '" alt="">'
  document.getElementById("photo-clue-img").style.height = $("#overlay-container").height() + "px";
  document.getElementById("overlay-container").style.overflow = "hidden";
}

function hideOverlay() {
  document.getElementById("overlay-container").style.display = "none";
  document.getElementById("overlay-container").style.overflow = "hidden";
  document.getElementById("underlay-container").style.filter = "none";
  document.getElementById("overlay-container").style.height = "calc(96% - 113px);";
  document.getElementById("welcome-container").style.display = "none";
  document.getElementById("qr-scanner-container").style.display = "none";
  document.getElementById("leaderboard-container").style.display = "none";
  document.getElementById("map-container").style.display = "none";
  document.getElementById("achievements-container").style.display = "none";
  document.getElementById("chatbot-container").style.display = "none";
  document.getElementById("photo-container").style.display = "none";
  document.getElementById("overlay-container").style.width = "80%";
  document.getElementById("overlay-container").style.borderWidth = "2vh";
  document.getElementById("overlay-container").style.left = "10%";
  document.getElementById("overlay-container").style.top = "4%";
}

function showOverlay() {
  document.getElementById("overlay-container").style.display = "block";
  document.getElementById("overlay-container").style.borderStyle = "solid";
  document.getElementById("underlay-container").style.filter = "blur(10px)";
  document.getElementById("overlay-container").style.height = "75%";
  document.getElementById("overlay-container").style.width = "80%";
  document.getElementById("overlay-container").style.top = "5%";
  document.getElementById("overlay-container").style.overflow = "hidden";
  document.getElementById("overlay-container").style.backgroundColor = "#ACCEEA";
}

function resetButtonColours() {
  document.getElementById("checkin-button").style.backgroundColor = "#005AA8";
  document.getElementById("leaderboard-button").style.backgroundColor = "#508CA4";
  document.getElementById("map-button").style.backgroundColor = "#508CA4";
  document.getElementById("achievements-button").style.backgroundColor = "#508CA4";
  document.getElementById("chatbot-button").style.backgroundColor = "#508CA4";
}

function underlaySelected() {
  if(document.getElementById("overlay-container").style.display != "none") {
    hideOverlay();
    resetButtonColours();
  }
}
