//jquery for loading all paymetns list
$(document).ready( function () {
    var pages = 1
    function tableData(page=1, trans_type='', balanced='', date=', ', search = '', trans_id=''){
        var header = "Payment for All Transactions"
        if(trans_type=='STOCK+IN'){
            header = 'Payment for Stock Bought Transactions'
        }else if(trans_type=='STOCK+OUT'){
            header = 'Payment for Stock Sold Transactions'
        }else{
            header = header
        }
        if (date != ', ') {
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/payments/?page=${page}&transaction___type=${trans_type}&transaction__balanced=${balanced}&date__date__range=${date}&search=${search}&transaction__id=${trans_id}`
        }else{
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/payments/?page=${page}&transaction___type=${trans_type}&transaction__balanced=${balanced}&search=${search}&transaction__id=${trans_id}`
        }
        var td = ''
        $.ajax({
            url:url,
            method:"GET",
            data:{},
            success:function(data){
                $("#header").html(`${header} (${data.count})`)//update count on header
                var paymt = data.results
                pages = Math.ceil(data.count/5)
                if (pages>=1){
                    paginationHtml(pages)
                }
                if (paymt.length >0){
                    $.each(paymt, function(e){
                        add_pay_btn = `<a href='${paymt[e].add_pay_url}' class="btn btn-warning btn-sm btn-block">Add Payment</a>`
                        view_edit_trans_btn = `<a href="${paymt[e].view_update_trans_url}" class="btn btn-sm btn-info btn-sm btn-block">View/ Edit</a>`
                        if(paymt[e].balanced){
                            add_pay_btn = `<a href='${paymt[e].add_pay_url}' class="btn btn-success btn-sm btn-block disabled">Balanced</a>`
                        }                        
                        tr = `
                        <tr>
                            <td>${paymt[e].date}</td>
                            <td>${paymt[e].trans_id}</td>
                            <td>${paymt[e].vendor_client}</td>
                            <td>${paymt[e].transaction}</td>
                            <td>Rs. ${paymt[e].amount}</td>
                            <td>
                                ${add_pay_btn}
                                ${view_edit_trans_btn}
                            </td>
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
    var trans_type = ''
    var balanced = ''
    var sdate = ''
    var edate = ''
    var date = sdate + ', ' +edate
    var trans_id = ''
    $("#id-search-filter").keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            page = 1
            trans_id = e.target.value
            tableData(page, trans_type, balanced, date, search, trans_id);
        }
    })
    $("#Transasction_Filter").change(function(e){
        page = 1
        trans_type = e.target.value
        tableData(page, trans_type, balanced, date, search, trans_id);
    })
    $("#Balance_Filter").change(function(e){
        page = 1
        balanced = e.target.value
        tableData(page, trans_type, balanced, date, search, trans_id);
    })
    $("#sdate-filter").change(function(e){
        page = 1
        sdate = e.target.value
        if (edate == '' || edate<sdate) {
            edate = sdate
        }
        date = sdate + ', ' +edate
        tableData(page, trans_type, balanced, date, search, trans_id);
    })
    $("#edate-filter").change(function(e){
        page = 1
        edate = e.target.value
        if (sdate == '' || sdate>edate) {
            sdate = edate
        }
        date = sdate + ', ' +edate
        tableData(page, trans_type, balanced, date, search, trans_id);
    })
    $("#search-filter").keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            page = 1
            search = e.target.value
            tableData(page, trans_type, balanced, date, search, trans_id);
        }
    })
    $("#clear-filter").click(function(){
        page = 1
        tableData(page=1, trans_type='', balanced='', date=', ', search = '', trans_id='')
        $("#filter-form")[0].reset()
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

    $('.pagination-span').on('click', '#previousBtn', function (){
        page = page>1?page-1:page
        tableData(page, trans_type, balanced, date, search, trans_id);
    });
    $('.pagination-span').on('click', '#nextBtn', function (){
        page = page!=pages?page+1:page
        tableData(page, trans_type, balanced, date, search, trans_id);
    });    
    
    $('#table_id').on('click', '#modal-item', function (e){
        e.preventDefault();
        var item_id = e.target.attributes.value.value
        get_item_info_trans(item_id)
    });
});