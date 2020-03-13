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
      document.getElementById("leaderboard-container").style.display = "block";
      document.getElementById("overlay-container").style.overflow = "hidden";
      loadTeamLeaderboard();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("leaderboard-button").style.backgroundColor = "orange";
    document.getElementById("leaderboard-container").style.display = "block";
    document.getElementById("overlay-container").style.overflow = "hidden";
    loadTeamLeaderboard();
  }
}

function loadTeamLeaderboard(){
  document.getElementById("team-leaderboard-button").style.backgroundColor = "#6F97A7";
  document.getElementById("individual-leaderboard-button").style.backgroundColor = "#4B89A2";
  document.getElementById("team-leaderboard").style.display = "block";
  document.getElementById("individual-leaderboard").style.display = "none";

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("team-leaderboard").innerHTML = this.responseText;
  }
  };
  xhttp.open("GET", "/getTeamLeaderboard", true);
  xhttp.send();
  document.getElementById("overlay-container").style.backgroundColor = "#508CA4";
}

function loadIndividualLeaderboard() {
  document.getElementById("individual-leaderboard-button").style.backgroundColor = "#6F97A7";
  document.getElementById("team-leaderboard-button").style.backgroundColor = "#4B89A2";
  document.getElementById("individual-leaderboard").style.display = "block";
  document.getElementById("team-leaderboard").style.display = "none";

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("individual-leaderboard").innerHTML = this.responseText;
  }
  };
  xhttp.open("GET", "/getIndividualLeaderboard", true);
  xhttp.send();
  document.getElementById("overlay-container").style.backgroundColor = "#508CA4";
}
