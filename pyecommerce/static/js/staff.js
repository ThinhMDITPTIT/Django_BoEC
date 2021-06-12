var cancelbtn = document.getElementsByName("cancleorder");

var confirmbtn = document.getElementsByName("confirmorder");

var outdeliverybtn = document.getElementsByName("outdelivery");

var pending = document.getElementsByName("pending");

function orderHandler(shippingid,action){
    const url = "/handler_order/";

    fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ shippingid : shippingid , action : action}),
      })
        .then((response) => {
          console.log(response);
          return response.json();
        })
        .then((data) => {
          console.log("data:", data);
          location.reload();
        })
        .catch((error) => {
          location.reload();
          console.log("error: " + error);
        });
 };
 
 for(var i = 0; i < cancelbtn.length ; i++){
    cancelbtn[i].addEventListener('click',function(){
        var shippingid = this.dataset.shippingid;
        var action = this.dataset.action;
        orderHandler(shippingid,action);
    });
 }

 for(var i = 0; i < confirmbtn.length ; i++){
    confirmbtn[i].addEventListener('click',function(){
        var shippingid = this.dataset.shippingid;
        var action = this.dataset.action;
        orderHandler(shippingid,action);
    });
 }

 for(var i = 0; i < outdeliverybtn.length ; i++){
    outdeliverybtn[i].addEventListener('click',function(){
        var shippingid = this.dataset.shippingid;
        var action = this.dataset.action;
        orderHandler(shippingid,action);
    });
 }

 for(var i = 0; i < pending.length ; i++){
    pending[i].addEventListener('click',function(){
        var shippingid = this.dataset.shippingid;
        var action = this.dataset.action;
        orderHandler(shippingid,action);
    });
 }