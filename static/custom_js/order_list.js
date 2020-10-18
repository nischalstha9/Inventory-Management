//jquery for loading all transaction list
$(document).ready( function () {
    var pages = 1
    function tableData(page=1, status='', date=', ', search = '', order_id=''){
        var header = "Online Orders"
        if(status=='CO'){
            header = 'Confirmed Orders'
        }else if(status=='S'){
            header = 'Fulfilled Orders'
        }else if(status=='CA'){
            header = 'Cancalled Orders'
        }else{
            header = header
        }
        if (date != ', ') {
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/orders/?page=${page}&status=${status}&ordered_date__date__range=${date}&search=${search}&id=${order_id}`
        }else{
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/orders/?page=${page}&status=${status}&search=${search}&id=${order_id}`
        }
        var td = ''
        $.ajax({
            url:url,
            method:"GET",
            data:{},
            success:function(data){
                $("#header").html(`${header} (${data.count})`)//update count on header
                var orders = data.results
                pages = Math.ceil(data.count/5)
                if (pages>=1){
                    paginationHtml(pages)
                }
                if (orders.length >0){
                    $.each(orders, function(e){
                        status = orders[e].status
                        status_html = status=='O'?"<span class='badge badge-danger'>Ordered</span>":status=='CO'?"<span class='badge badge-warning'>Confirmed</span>":status=='S'?"<span class='badge badge-success'>Fulfilled</span>":"<span class='badge badge-dark'>Cancelled</span>" 
                        tr = `
                        <tr>
                            <td>${orders[e].id}</td>
                            <td>${orders[e].ordered_date}</td>
                            <td>${orders[e].user}</td>
                            <td>
                            ${status_html}
                            </td>
                            <td><a href='${orders[e].detail_url}' class='btn btn-sm btn-outline-dark'>View</a></td>
                        </tr>
                        `
                        td += tr
                    })

                }
                $("tbody").html(td)

            },
            error: function(error){
                console.log(error);
            }
        })
    }
    tableData()
    var search = ''
    var page = 1
    var status = ''
    var sdate = ''
    var edate = ''
    var order_id = ''
    var date = sdate + ', ' +edate
    $("#status_filter").change(function(e){
        page = 1
        status = e.target.value
        tableData(page, status, date, search, order_id);
    })
    $("#sdate-filter").change(function(e){
        page = 1
        sdate = e.target.value
        if (edate == '' || edate<sdate) {
            edate = sdate
        }
        date = sdate + ', ' +edate
        tableData(page, status, date, search, order_id);
    })
    $("#edate-filter").change(function(e){
        page = 1
        edate = e.target.value
        if (sdate == '' || sdate>edate) {
            sdate = edate
        }
        date = sdate + ', ' +edate
        tableData(page, status, date, search, order_id);
    })
    $("#search-filter").keypress(function(e){
        if(e.which == 13){
            e.preventDefault();
            page = 1
            search = e.target.value
            tableData(page, status, date, search, order_id);
        }
    })
    $("#id-search-filter").keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            page = 1
            order_id = e.target.value
            tableData(page, status, date, search, order_id);
        }
    })
    $("#clear-filter").click(function(){
        page = 1
        $("#filter-form")[0].reset()
        tableData(page=1, status='', date=', ', search = '', order_id='')
    })

    //build pagination
    function paginationHtml(pages){
        var next = (page==pages)?"<li class='page-item disabled'><a class='page-link' href='# id='nextBtn'>Next</a></li>":"<li class='page-item'><a class='page-link' href='#' id='nextBtn'>Next</a></li>"
        var prev = (page==1)?"<li class='page-item disabled'><a class='page-link' href='#' id='previousBtn' tabindex='-1'>Previous</a></li>":"<li class='page-item'><a class='page-link' href='#' id='previousBtn' tabindex='-1'>Previous</a></li>"
        var temp = `
        <nav aria-label="...">
        <ul class="pagination">
            ${prev}
            ${next}
        </ul>
        </nav>
        `
        $(".pagination-span").html(temp);
    }
    $('.pagination-span').on('click', '#previousBtn', function (e){
        e.preventDefault()
        page = page>1?page-1:page
        tableData(page, status, date, search, order_id);
    });
    $('.pagination-span').on('click', '#nextBtn', function (e){
        e.preventDefault()
        page = page!=pages?page+1:page
        tableData(page, status, date, search, order_id);
    });
});