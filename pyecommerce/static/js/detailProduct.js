var addtocartBtn = document.getElementById('addtocartBtn');

var radioBtns = document.getElementsByName('size-option');

var quantityElement = document.getElementById('quantity');

function getSizeOption(){
    var size = '';
    for(var i = 0; i < radioBtns.length; i++){
        if(radioBtns[i].checked){
            size=radioBtns[i].value;
        }
    }
    console.log(size);
    return size;
}

function getQuantity(){
    var quantity = 1;
    quantity = quantityElement.value;
    console.log(quantity);
    return quantity;
}

addtocartBtn.addEventListener('click', function(){
    if(user == 'AnonymousUser'){
        alert('You can login to puncharse product');
    }
    else{
        var productid = this.dataset.product;
        var action = this.dataset.action;
        var size = getSizeOption();
        var quantity = getQuantity();
        addToCart(action, productid, size, quantity);
    }
})

function addToCart(action, productid, size, quantity){
    var url = "/add_to_cart/";
    fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ action: action, productid: productid, size:size, quantity:quantity }),
      })
        .then((response) => {
          console.log(response);
          return response.json();
          location.reload();
        })
        .then((data) => {
          console.log("data:", data);
          location.reload();
        })
        .catch((error) => {
          location.reload();
          console.log("error: " + error);
        });
}