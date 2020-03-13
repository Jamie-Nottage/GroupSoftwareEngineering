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
      document.getElementById("overlay-container").style.overflow = "scroll";
      loadAchievements();
    }
  } else {
    hideOverlay();
    showOverlay();
    document.getElementById("achievements-button").style.backgroundColor = "orange";
    document.getElementById("achievements-container").innerHTML = '<div class="loader"></div>';
    document.getElementById("overlay-container").style.overflow = "scroll";
    loadAchievements();
  }
}

function loadAchievements(wait=false) {
  document.getElementById("achievements-container").style.display = "block";
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
      achievementContent = this.responseText;
      if(wait){
        setTimeout(function() {
          document.getElementById("achievements-container").innerHTML = achievementContent;
          $(".achievement-answer-button").click(answerButtonClicked);
        }, 500)
      } else {
        document.getElementById("achievements-container").innerHTML = this.responseText;
        $(".achievement-answer-button").click(answerButtonClicked);
      }
  }
  };
  xhttp.open("GET", "/displayAchievements", true);
  xhttp.send();
}

function achievementQButtonPressed(e) {
  // Dropdown is up
  if($(e).css("background-color") == "rgb(75, 137, 162)") {
    hideAllAchievementDropdowns()
    $(e).css("background-color", "#6f97a7");
    $(e).next().css("display", "block");

  // Dropdown is down
  } else {
    $(e).css("background-color", "#4B89A2");
    $(e).next().css("display", "none");
  }
}

function hideAllAchievementDropdowns() {
  $(".achievement-right.incomplete").css("background-color", "#4B89A2")
  $(".quiz-dropdown").css("display", "none");
}

function answerButtonClicked(e) {
  // Code to temporarily disable event listeners
  currentButton = this;
  while ($(currentButton).html() != undefined) {
    $(currentButton).off("click");
    currentButton = $(currentButton).next(".achievement-answer-button");
  }
  currentButton = $(this).prev(".achievement-answer-button");
  while ($(currentButton).html() != undefined) {
    $(currentButton).off("click");
    currentButton = $(currentButton).prev(".achievement-answer-button");
  }
  questionTitle = $(this).prevAll(".achievement-question-txt").html()

  currentButton = this;
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    if(this.responseText == "true") {
      currentButton.style.backgroundColor = "green";
      loadAchievements(true);
    } else {
      currentButton.style.backgroundColor = "red";
      loadAchievements(true);
    }
  }
  };
  xhttp.open("POST", "/sendQuizAnswer", true);
  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  xhttp.send("answer="+this.innerHTML+"&questionTitle=" + questionTitle);
}
