var searchVal = document.getElementById('searchInput');
var searchBtn = document.getElementById('searchBtn');

searchBtn.addEventListener('click', function () {
 if (
   searchVal.value != 'Man' &&
   searchVal.value != 'Woman' &&
   searchVal.value != 'Croptop' &&
   searchVal.value != 'Pants' &&
   searchVal.value != 'Shoes' &&
   searchVal.value != 'Equipments' &&
   searchVal.value != 'Jackets'
 ) {
   alert("Do not found anything!");
   // var urlName = '/product/' + searchVal.value;
   // window.location.href = urlName;
   searchVal.value = '';
 } else {
   var urlTag = '/product/' + searchVal.value;
   window.location.href = urlTag;
   searchVal.value = '';
 }
});

