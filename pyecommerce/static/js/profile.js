var emailinput = document.getElementById('emailinput');

var phoneinput = document.getElementById('phoneinput');

var addressinput = document.getElementById('addressinput');

var dobinput = document.getElementById('dobinput');

var savebtn = document.getElementById("savebtn");

var cancelbtn = document.getElementsByName("cancleorder");

var confirmbtn = document.getElementsByName("confirmorder");

function setReadonly(idelement){
    var inputelement = document.getElementById(idelement);
    if(inputelement.readOnly){
        inputelement.readOnly = false;
    }
    else{
        inputelement.readOnly = true;
    }
}

emailinput.addEventListener('change', function(){
    savebtn.disabled = false;
});

if(dobinput != null){
    dobinput.addEventListener('change',function(){
        savebtn.disabled = false;
        console.log(dobinput.value)
    })
}

phoneinput.addEventListener('change', function(){
    savebtn.disabled = false;
});
addressinput.addEventListener('change', function(){
    console.log(savebtn.disabled)
    savebtn.disabled = false;
});
 function updateCustomerInf(phone, email, address, dob){
     var emailvalue = "";
     var phonevalue = "";
     var addressvalue = "";
     var dobvalue = "";
     console.log(dob);
     var emailinputvalue = emailinput.value;
     var phoneinputvalue = phoneinput.value;
     var addressinputvalue = addressinput.value;
     if(dobinput != null){
        var dobinputvalue = dobinput.value;
        dobvalue = dobinputvalue;
     }else{
        var dobconvert = moment(dob).format('YYYY-MM-DD');
        dobvalue = dobconvert;
     }
    if(email !== emailinputvalue){
       emailvalue = emailinputvalue
    }
    else{
        emailvalue = email;
    }
    if(phone !== phoneinputvalue){
        phonevalue = phoneinputvalue
    }
    else{
        phonevalue = phone;
    }
    if(address !== addressinputvalue){
        addressvalue = addressinputvalue
    }
    else{
        addressvalue = address;
    }
    updateInf(emailvalue,dobvalue,phonevalue,addressvalue);
 };

 function updateInf(email,dob,phone,address){
    var url = "/update_customer_inf/";

    fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ email: email, dob: dob, phone: phone, address:address}),
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

 function cancleOrder(shippingid,action){
    const url = "/cancel_order/";

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
        cancleOrder(shippingid,action);
    });
 }

 for(var i = 0; i < confirmbtn.length ; i++){
    confirmbtn[i].addEventListener('click',function(){
        var shippingid = this.dataset.shippingid;
        var action = this.dataset.action;
        cancleOrder(shippingid,action);
    });
 }
