let buy = $('button');

let price = $('.percentChange');
let total = 0
$('#mytable .percentChange').each(function() {
    var test = ($(this).text());
    test = test.replace('$', '');
    total += +test
    
    
  });
console.log(total);


buy.click(function(){
    $(this).text("confirm")
    
    let id = $(this).attr('id');
    let lbl =  $('#' + id + '-label');
    lbl.addClass('selected');
    let shares = $('#' + id + '-shares');
    shares.addClass('selected');
    let div = $('#' + id);
    div.html('<button id="{{ stocks[i] }}" class="submit-button" type="submit">Confirm</button>')

});