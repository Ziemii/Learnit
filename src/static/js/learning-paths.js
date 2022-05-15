
    
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


function byRating(){
    var ratingOrder = localStorage.getItem('ratingOrder');
    if(ratingOrder){
        localStorage.setItem('ratingOrder', ratingOrder*-1);
    }
    else {
        localStorage.setItem('ratingOrder', 1);
    }
    if(ratingOrder > 0){
        window.location.href = '/learning-paths?sortBy=rating';
    }
    else{
        window.location.href = '/learning-paths?sortBy=!rating';
    }
}

function byAlpha(){
    var alphaOrder = localStorage.getItem('alphaOrder');
    if(alphaOrder){
        localStorage.setItem('alphaOrder', alphaOrder*-1);
    }
    else {
        localStorage.setItem('alphaOrder', 1);
    }
    if(alphaOrder > 0){
        window.location.href = '/learning-paths?sortBy=alpha';
    }
    else{
        window.location.href = '/learning-paths?sortBy=!alpha';
    }
    

}

function Search(){
    console.log(document.getElementById('search').innerHTML);
    // window.location.href = '/learning-paths?search=' + document.getElementById('search').innerText;

}