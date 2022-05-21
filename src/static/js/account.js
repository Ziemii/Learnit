var wait = (ms) => {
    const start = Date.now();
    let now = start;
    while (now - start < ms) {
      now = Date.now();
    }
}
function removeBookmark(pathId){
    var url = "/bookmark";
    var params = "userId="+$('#pathData').data('userid')+"&pathId="+pathId;
    console.log(params)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params)
    wait(200);
    return location.reload();
}
function removeSubmission(pathId){
    if (confirm('Are you sure you want to delete this submission from database?')) {
        // Save it!
        var url = "/delete";
        var params = "pathId="+pathId;
        console.log(params)
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
    
        //Send the proper header information along with the request
        xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

        xhr.send(params)
        wait(200);
        document.getElementById(pathId).remove();
        // return location.reload();
    } else {
        // Do nothing!
      }
    
}