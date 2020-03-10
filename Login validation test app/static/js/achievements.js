function achievementQButtonPressed(e) {
  // Dropdown is up
  if($(e).css("background-color") == "rgb(75, 137, 162)") {
    $(e).css("background-color", "#6f97a7");

  // Dropdown is down
  } else {
    $(e).css("background-color", "#4B89A2")
  }
}
