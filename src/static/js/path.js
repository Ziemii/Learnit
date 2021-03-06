// JavaScript adding functionality to learning path page

// Delay mechanism
var wait = (ms) => {
  const start = Date.now();
  let now = start;
  while (now - start < ms) {
    now = Date.now();
  }
};

// Transforms tags from pure string to interactive buttons
let cardsTags = document.getElementsByName("tags");

cardsTags.forEach((rawTag) => {
  let tags = rawTag.innerHTML.split("#");
  rawTag.innerHTML = "";
  tags.forEach((element) => {
    if (element == "") {
      return;
    }
    var hyperlink = document.createElement("a");
    hyperlink.href = "/learning-paths?tag=" + element;
    var button = document.createElement("button");
    button.setAttribute("class", "btn btn-outline-primary btn-sm m-1");
    var inside = document.createTextNode("#" + element);
    button.appendChild(inside);
    hyperlink.appendChild(button);

    rawTag.appendChild(hyperlink);
  });
});

// Endorse and bookmark buttons tooltip initialization
$(function () {
  $('[data-toggle="tooltip"]').tooltip({ placement: "right" });
});

// Sends API request to save endorsement in database
function rate() {
  var url = "/rate";
  var params =
    "userId=" +
    $("#pathData").data("userid") +
    "&pathId=" +
    $("#pathData").data("pathid");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  xhr.send(params);
  wait(200);
  return location.reload();
}

// Sends API request to save bookmark in user's bookmarks
function bookmark() {
  var url = "/bookmark";
  var params =
    "userId=" +
    $("#pathData").data("userid") +
    "&pathId=" +
    $("#pathData").data("pathid");
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);

  xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

  xhr.send(params);
  wait(200);
  return location.reload();
}
