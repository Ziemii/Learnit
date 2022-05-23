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
     
    
}
function deleteAccount(userId){
    
        const url = "./deleteAccount";
        fetch(url, {
            method: 'post',
            body: JSON.stringify(userId),
            mode: 'cors',
            headers: new Headers({
              'Content-Type': 'application/json'
            })
          })
            .then(
                response => console.log(response.text())
            ).then(
                window.location.href = './logout'
            ).catch (function (error) {
                console.log('Request failed', error);
                });
            
}
$(function () {
  $('[data-toggle="tooltip"]').tooltip({ placement: "right" });
});