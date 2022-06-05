// Adding simple functionality to control panel

// Sends API request with information if submission was accepted or rejected
function verdict(verdict, id) {
    var url = "/verdict";
    var params =
      "verdict=" +
      verdict +
      "&pathId=" +
      id;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
  
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  
    xhr.send(params);
    wait(200);
    return location.reload();
  }