$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});
$('#pass-check').keyup(function () {
   if ($('#pass').val() == $('#pass-check').val()) {
      $('#pass').removeClass('pass-non');
      $('#pass-check').removeClass('pass-non');
      $('#pass').addClass('pass');
      $('#pass-check').addClass('pass');
   } else{
      $('#pass').addClass('pass-non');
      $('#pass-check').addClass('pass-non');
   }
 });