// navbar toggle
AOS.init();
M.AutoInit();

$(document).ready(function () {
  $(".sidenav").sidenav();
  $('select').formSelect();
  $('input#input_text, textarea#comment').characterCounter();
  $('.datepicker').datepicker();
});
  
$('.dropdown-trigger').dropdown({
  "hover":true,
  "constrainWidth": false,
  "inDuration": 200,
  "outDuration": 225,
  "coverTrigger":false,
  "isScrollable":false	
});