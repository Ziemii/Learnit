let cardsTags = document.getElementsByName('tags');

cardsTags.forEach(rawTag => {
    let tags = rawTag.innerHTML.split('#');
    rawTag.innerHTML='';
    tags.forEach(element => {
            if(element==""){return;} 
            var hyperlink = document.createElement("a");
            hyperlink.href = '/learning-paths?tag=' + element;
            var button = document.createElement("button");
            button.setAttribute('class', 'btn btn-outline-primary btn-sm m-1');
            var inside = document.createTextNode('#'+element);
            button.appendChild(inside);
            hyperlink.appendChild(button);
            
            rawTag.appendChild(hyperlink);
        })
})

$(function () {
    $('[data-toggle="tooltip"]').tooltip({placement:'right'})
  })

function rate(){
    var url = "/rate";
    var params = "userId="+$('#pathData').data('userid')+"&pathId="+$('#pathData').data('pathid');
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    
    //Send the proper header information along with the request
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(params);
    location.reload();
}
// var ele = document.getElementById('pathData');
// console.log($(ele).data());
// var pathData = $('#pathData').data();
// console.log("userId="+$('#pathData').data('userid')+"&pathId="+$('#pathData').data('pathid'))