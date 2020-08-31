/* globals Chart:false, feather:false */

let price = $('.percentChange');
let total = 0;
let balance = $('#balance').html();
console.log(balance)
//get balance

$( document ).ready(function() {
$('#mytable .percentChange').each(function() {
    var change = ($(this).text());
    change = change.replace('$', '');
    total += +change
  });
  total += +$('#balance').html()
  total = total.toFixed(2);
  
  $('#balance').html('Balance: ' + total);
  sell(total);
});

function sell(balance){
  let sell = $('.sell')
  sell.click(function(){
    document.getElementById("myForm").style.display = "block";
   
    let shares = $(this).closest("tr").find('.shares').text();
    let price = $(this).closest("tr").find('.currentPrice').text();
    let name = $(this).closest("tr").find('.name').text();
    $('.sellName').val(name);
    $('.sellPrice').val(+price);
    $('.currBalance').val(balance); 
    $('#stock-name').html('Sell ' + name + '?');
    $('.sellShares').attr("max", shares);
    console.log($('.sellName').val());
    console.log($('.sellPrice').val());
  })};
    
    

    



function closeForm() {
  document.getElementById("myForm").style.display = "none";};

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday'
      ],
      datasets: [{
        data: [
          15339,
          21345,
          18483,
          24003,
          23489,
          24092,
          12034
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}())
