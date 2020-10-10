//jquery for loading all transaction list
$(document).ready( function () {
    var pages = 1
    function tableData(page=1, trans_type='', balanced='', date=', ', search = '', trans_id=''){
        var header = "All Transactions"
        if(trans_type=='STOCK+IN'){
            header = 'Stock Bought Transactions'
        }else if(trans_type=='STOCK+OUT'){
            header = 'Stock Sold Transactions'
        }else{
            header = header
        }
        if (date != ', ') {
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/transactions/?page=${page}&_type=${trans_type}&balanced=${balanced}&date__date__range=${date}&search=${search}&id=${trans_id}`
        }else{
            var url = `${window.location.protocol}//${window.location.host}/inventory/api/transactions/?page=${page}&_type=${trans_type}&balanced=${balanced}&search=${search}&id=${trans_id}`
        }
        var td = ''
        $.ajax({
            url:url,
            method:"GET",
            data:{},
            success:function(data){
                $("#header").html(`${header} (${data.count})`)//update count on header
                var trans = data.results
                pages = Math.ceil(data.count/5)
                if (pages>=1){
                    paginationHtml(pages)
                }
                if (trans.length >0){
                    $.each(trans, function(e){
                        bal_or_rem = `<span class="badge badge-danger">Rs. ${ trans[e].remaining_payment } remaining</span>`
                        pay = `<a href="${trans[e].pay_url}" class="btn btn-sm btn-warning btn-small btn-block">Add Payment</a><a class='btn mt-1 btn-sm btn-info btn-block' href="${trans[e].update_url}">View/Edit</a>`
                        if(trans[e].balanced){
                            bal_or_rem = `<span class="badge badge-success">BALANCED</span>`
                            pay = `<a href="#" class="btn btn-sm btn-dark disabled btn-block">BALANCED</a><a class='btn mt-1 btn-sm btn-info btn-block' href="${trans[e].update_url}">View/Edit</a>`
                        }                        
                        tr = `
                        <tr>
                            <td>${trans[e].date}</td>
                            <td>${trans[e].id}</td>
                            <td>${trans[e].vendor_client}</td>
                            <td><a id='modal-item' href='#' value='${trans[e].item_id}'>${trans[e].item}</a></td>
                            <td>${trans[e]._type}</td>
                            <td>${trans[e].quantity}</td>
                            <td>Rs. ${trans[e].cost}</td>
                            <td>Rs. ${trans[e].payable}</td>
                            <td>
                                Rs. ${trans[e].paid}${bal_or_rem}
                            </td>
                            <td>
                                ${pay}
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
    var trans_id = ''
    var date = sdate + ', ' +edate
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
        if(e.which == 13){
            e.preventDefault();
            page = 1
            search = e.target.value
            tableData(page, trans_type, balanced, date, search, trans_id);
        }
    })
    $("#id-search-filter").keypress(function(e){
        if(e.which == 13) {
            e.preventDefault();
            page = 1
            trans_id = e.target.value
            tableData(page, trans_type, balanced, date, search, trans_id);
        }
    })
    $("#clear-filter").click(function(){
        page = 1
        $("#filter-form")[0].reset()
        tableData(page=1, trans_type='', balanced='', date=', ', search = '', trans_id='')
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
        tableData(page, trans_type, balanced, date, search, trans_id);
    });
    $('.pagination-span').on('click', '#nextBtn', function (e){
        e.preventDefault()
        page = page!=pages?page+1:page
        tableData(page, trans_type, balanced, date, search, trans_id);
    });
    $('#table_id').on('click', '#modal-item', function (e){
        e.preventDefault();
        var item_id = e.target.attributes.value.value
        get_item_info_trans(item_id)
    });
});