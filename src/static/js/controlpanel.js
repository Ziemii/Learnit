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