$(document).ready( function () {
    var pages = 1
    function tableData(page=1, trans_type='', balanced='', date=''){
        var header = "All Transactions"
        if (date != ', ') {
            var url = `http://${window.location.host}/inventory/api/transactions/?page=${page}&_type=${trans_type}&balanced=${balanced}&date__date__range=${date}`
        }else{
            var url = `http://${window.location.host}/inventory/api/transactions/?page=${page}&_type=${trans_type}&balanced=${balanced}`
        }
        var td = ''
        $.ajax({
            url:url,
            method:"GET",
            data:{},
            success:function(data){
                var trans = data.results
                pages = Math.ceil(data.count/1)
                if (pages>1){
                    paginationHtml(pages)
                }
                if (trans.length >0){
                    $.each(trans, function(e){
                        bal_or_rem = `<span class="badge badge-danger">Rs. ${ trans[e].remaining_payment } remaining</span>`
                        pay = `<a href="${trans[e].pay_url}" class="btn btn-sm btn-warning btn-small">Add Payment</a>`
                        if(trans[e].balanced){
                            bal_or_rem = `<span class="badge badge-success">BALANCED</span>`
                            pay = `<a href="#" class="btn btn-sm btn-success btn-success">BALANCED</a>`
                        }                        
                        tr = `
                        <tr>
                            <td>${trans[e].date}</td>
                            <td>${trans[e].vendor_client}</td>
                            <td><a href="${trans[e].update_url}">${trans[e].item}</a></td>
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
    var page = 1
    var trans_type = ''
    var balanced = ''
    var sdate = ''
    var edate = ''
    var date = sdate + ', ' +edate
    $("#Transasction_Filter").change(function(e){
        trans_type = e.target.value
        tableData(page, trans_type, balanced, date);
    })
    $("#Balance_Filter").change(function(e){
        balanced = e.target.value
        tableData(page, trans_type, balanced, date);
    })
    $("#sdate-filter").change(function(e){
        sdate = e.target.value
        if (edate == '') {
            edate = sdate
        }
        date = sdate + ', ' +edate
        tableData(page, trans_type, balanced, date);
    })
    $("#edate-filter").change(function(e){
        edate = e.target.value
        if (sdate == '') {
            sdate = edate
        }
        date = sdate + ', ' +edate
        tableData(page, trans_type, balanced, date);
    })


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
        tableData(page, trans_type, balanced, date);
    });
    $('.pagination-span').on('click', '#nextBtn', function (){
        page = page!=pages?page+1:page
        tableData(page, trans_type, balanced, date);
    });    
});