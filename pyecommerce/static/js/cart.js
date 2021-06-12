// add to cart on store component
var updateBtns = document.getElementsByClassName("update-cart");

for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var option = this.dataset.size;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      console.log("User is not authenticated");
    } else {
      updateUserOrder(productId, action, option);
    }
  });
}
// request to server
function updateUserOrder(productId, action, option) {
  console.log("User is authenticated, sending data ...");
  var url = "/update_item/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action, option:option }),
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
}

//change in cart component
var onchangeQuantity = document.getElementsByName("onchangeQuantity");

for (i = 0; i < onchangeQuantity.length; i++) {
  onchangeQuantity[i].addEventListener("change", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var quantityValue = this.value;
    var option = this.dataset.size;
    console.log(
      "productId:",
      productId,
      "Action:",
      action,
      "quantityValue",
      quantityValue,
      "option:",
      option
    );
    console.log("USER:", user);
    if (user == "AnonymousUser") {
      console.log("User is not authenticated");
    } else {
      updateQuantityItem(productId, action, quantityValue, option);
    }
  });
}
// request to server
function updateQuantityItem(productId, action, quantity, option) {
  console.log("User is authenticated, sending data ...");
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({
      productId: productId,
      option: option,
      action: action,
      quantity: quantity,
    }),
  })
    .then((response) => {
      console.log(response.body);
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
}
// on delete order-item
var ondeleteOrderItem = document.getElementsByName("ondeleteOrderItem");
// request to server

for (i = 0; i < ondeleteOrderItem.length; i++) {
  ondeleteOrderItem[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    var option = this.dataset.size;
    console.log("productId:", productId, "Action:", action);

    console.log("USER:", user);
    if (user == "AnonymousUser") {
      console.log("User is not authenticated");
    } else {
      deleteOrderItem(productId, action, option);
    }
  });
}
function deleteOrderItem(productId, action,option) {
  console.log("User is authenticated, sending data ...");
  var url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action, option:option}),
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
}

// update size option
var radioBtn = document.getElementsByClassName("size");
console.log(radioBtn);

for(var i = 0 ; i < radioBtn.length ; i++){
  console.log(radioBtn[i].checked);
  radioBtn[i].addEventListener('change',function(){
    if(this.checked == true){
      var productId = this.dataset.product;
      var changedoption = this.value;
      var rawoption = this.dataset.size;
      updateOptionOrderItem(productId,changedoption, rawoption);
    }
  })
}


function updateOptionOrderItem(productId, size,rawoption) {
    console.log("User is authenticated, sending data ...");
    var url = "/update_item/";
    const action = "changeoption";
  
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action, changedoption:size, option:rawoption }),
    })
      .then((response)=>{
        const results = response.json();
        console.log(results);
        location.reload();
      }).then((data)=>{
        console.log("Data is ok", data);
      })
      .catch((error) => {
        location.reload();
        console.log("error: " + error);
      });
  }
