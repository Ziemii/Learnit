



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