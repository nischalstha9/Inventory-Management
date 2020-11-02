const host = window.location.host
const protocol = window.location.protocol
const itemUrl = `${protocol}//${host}/inventory/item-quantity/?format=json`
var Items = []
var Item_count = []
$.ajax({
    url: itemUrl,
    method : "GET",
    data:{},
    success: function(data){
        data.forEach(element => {
            Items.push(element.name)
            Item_count.push(element.quantity)
        });

        var ctx = document.getElementById('itemChart');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Items,
                datasets: [{
                    label: 'Items in Inventory',
                    data: Item_count,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

    },
    error: function(error){
    console.log(error)
    }
});
const transactionUrl = `${protocol}//${host}/inventory/dashboard/?format=json`
$.ajax({
    url: transactionUrl,
    method : "GET",
    data:{},
    success: function(data){
        //balanced and Unbalanced chart4
        var ctx = document.getElementById('totalTransactionsChart');
        var myChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Balanced Stock In Transactions', 'Pending Stock In Transactions', 'Balanced Stock Out Transactions', 'Pending Stock Out Transactions'],
                datasets: [{
                    data: [data.balanced_dr_trans, data.unpaid_dr_trans, data.balanced_cr_trans, data.unpaid_cr_trans],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth:1
                }]
            },
            options: {
                
            }
        });
        //transactionCountTodayChart
        var ctx = document.getElementById('transactionCountTodayChart');
        var myChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ["Today's Item Bought Count", "Today's Item Sold Count"],
                datasets: [{
                    data: [5,6],
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                    ],
                    borderColor: [
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                    ],
                    borderWidth: 1
                }]
            },
            options: {

            }
        });
        //today Payment Chart
        var ctx = document.getElementById('paymentTodayChart');
        var myChart = new Chart(ctx, {
            type: 'polarArea',
            data: {
                labels: ['Payment for Sold Stock', 'Payment for Bought Stock'],
                datasets: [{
                    data: [5,6],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth:1
                }]
            },
            options: {
                
            }
        });
        //todays highest payment and sales
        var ctx = document.getElementById('todayHighestPaysChart');
        var myChart = new Chart(ctx, {
            type: 'horizontalBar',
            data: {
                labels: ['Todays Highest Payments'],
                datasets: 
                [
                    {
                        
                    label: "Today's Highest Payment Paid",
                    data: [data.today_highest_pay_sent,],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                        ],
                        borderWidth: 1
                    },
                    {
                    label: "Today's Highest Payment Received",
                    data: [data.today_highest_pay_received,],
                    backgroundColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                    borderColor: [
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)',
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                    ],
                    borderWidth: 1
                    },
                ]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });       

    },
    error: function(error){
    console.log(error)
    }
});