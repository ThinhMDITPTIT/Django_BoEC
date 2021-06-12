var addcommentbutton = document.getElementById("addcomment")
addcommentbutton.addEventListener('click', function(){
    var commentcontent = document.getElementById("commentcontent").value;
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log(commentcontent + " by:" + user);
    if(user == 'AnonymousUser'){
        console.log('User is not authenticated')
        return alert('Login before adding comment');
    }else{
        addComment(productId, action, commentcontent);
    }
});
function addComment(productId, action, commentcontent){
    console.log('User is authenticated, sending data ...');
    var url = '/add_comment/';

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action': action, 'content':commentcontent})
    })
    .then((response) =>{
        console.log(response);
        return response.json();
    })
    .then((data) =>{
        console.log('data:', data)
        location.reload();
    })
    .catch((error) => {    
        location.reload();
        console.log('error: ' + error)
    });
}