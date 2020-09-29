var host = window.location.host
var url = `http://${host}/inventory/cat_Count/?format=json`
var Categories = []
var Item_count = []
$.ajax({
    url: url,
    method : "GET",
    data:{},
    success: function(data){
        data.forEach(element => {
            Categories.push(element.name)
            Item_count.push(element.items_count)
        });

        var ctx = document.getElementById('categoryChart');
        var myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: Categories,
                datasets: [{
                    label: 'Items Per Categories',
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