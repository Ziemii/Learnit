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

function preview(){
    window.open('./preview', '_blank');
}

