$(document).ready( function () {
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
                if (trans.length >0){
                    $.each(trans, function(e){
                        tr = `
                        <tr>
                            <td>${trans[e].date}</td>
                            <td>${trans[e].vendor_client}</td>
                            <td><a href="${trans[e].update_url}">${trans[e].item}</a></td>
                            <td>${trans[e].quantity}</td>
                            <td>Rs. ${trans[e].cost}</td>
                            <td>Rs. ${trans[e].payable}</td>
                            <td>
                                Rs. ${trans[e].paid}<span class="badge badge-danger">Rs. ${ trans[e].remaining_payment } remaining</span>
                            </td>
                            <td>
                                <a href="${trans[e].pay_url}" class="btn btn-warning btn-small">Add Payment</a>
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

    var page=1
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
        tableData(page, trans_type, balanced, sdate+', '+edate);
    })
    $("#edate-filter").change(function(e){
        edate = e.target.value
        if (sdate == '') {
            sdate = edate
        }
        tableData(page, trans_type, balanced, sdate+', '+edate);
    })
    


});