var timedSignUpdate = setInterval(setSign, 3000);

tn = "1";

function setSign() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("movable-sign-txt").innerHTML = this.responseText;
  }
  };
  xhttp.open("POST", "/getSign", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("teamname="+tn);
  updateVisitedLocations();
}

function updateVisitedLocations() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("central-list").innerHTML = this.responseText;
  }
  };
  xhttp.open("POST", "/getCentralTable", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("teamname="+tn);
}

function checkIn() {
  overlayContainer = document.getElementById("overlay-container");
  if(document.getElementById("overlay-container").style.display == "block"){
    hideOverlay();
  } else {
    showOverlay();
    document.getElementById("overlay-container").style.height = "1px";
    document.getElementById("overlay-container").style.width = "1px";
    document.getElementById("overlay-container").style.overflow = "visible";
  }

}

function hideOverlay() {
  overlayContainer.style.display = "none";
  document.getElementById("checkin-button").style.backgroundColor = "#005AA8";
  document.getElementById("underlay-container").style.filter = "blur(0px)";
  document.getElementById("overlay-container").style.height = "calc(96% - 113px)";
  document.getElementById("overlay-container").style.top = "4%";
}

function showOverlay() {
  overlayContainer.style.display = "block";
  document.getElementById("checkin-button").style.backgroundColor = "orange";
  document.getElementById("underlay-container").style.filter = "blur(10px)";
  document.getElementById("overlay-container").style.height = "40%";
  document.getElementById("overlay-container").style.top = "25%";
}
