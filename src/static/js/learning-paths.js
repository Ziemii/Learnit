
    
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
    searchWord = document.getElementById('search').value;
    // url = new URL(searchWord,'/learning-paths?search=');
    console.log(document.getElementById('search').value);
    window.location.href = '/learning-paths?search=' + searchWord;

}

const url = new URL(window.location);
const sort = url.searchParams.get('sortBy');
switch(sort){
    case 'alpha':
        var byAlphaBtn = document.getElementById('byAlpha').classList;
        byAlphaBtn.add('btn-success');
        byAlphaBtn.remove('btn-outline-success');
        byAlphaBtn.remove('btn-danger');
        break;
    case '!alpha':
        var byAlphaBtn = document.getElementById('byAlpha').classList;
        byAlphaBtn.add('btn-danger');
        byAlphaBtn.remove('btn-outline-success');
        break;
    case 'rating':
        var byRatingBtn = document.getElementById('byRating').classList;
        byRatingBtn.add('btn-success');
        byRatingBtn.remove('btn-outline-success');
        byRatingBtn.remove('btn-danger');
        break;
    case '!rating':
        var byRatingBtn = document.getElementById('byRating').classList;
        byRatingBtn.add('btn-danger');
        byRatingBtn.remove('btn-outline-success');
        break;
}
    