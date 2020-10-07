//jquery for loading transaction and item info on selection of item
function handleResponse(data){
    var html = ''
    var dr = data.unpaid_dr_trans
    var cr = data.unpaid_cr_trans
    var dr_table_data = ''
    var cr_table_data = ''
    var dr_head = ''
    var cr_head = ''
    if (dr.length >0){
        dr_head = '<h4>Stock Bought Unpaid Transactions</h4>'
        $.each(dr, function(e){
            var dr_data = 
            `
            <tr>
                <td>${dr[e].date}</td>
                <td>${dr[e].vendor_client}</td>
                <td>${dr[e].item}</td>
                <td>${dr[e].quantity}</td>
                <td>Rs. ${dr[e].payable}</td>
                <td>Rs. ${dr[e].paid}</td>
                <td><a href="http://127.0.0.1:8000/inventory/transactions/${dr[e].id}/quickpay/"><span class="badge badge-warning">Pay Rs. ${ dr[e].remaining_payment }</span></a></td>
            </tr>
            `
        dr_table_data += dr_data
        })
    }
    if (cr.length >0){
        cr_head = '<h4>Stock Sold Unpaid Transactions</h4>'
        $.each(cr, function(e){
            var cr_data = 
            `
            <tr>
                <td>${cr[e].date}</td>
                
                <td>${cr[e].vendor_client}</td>
                <td>${cr[e].item_id}</td>
                <td>${cr[e].quantity}</td>
                <td>Rs. ${cr[e].payable}</td>
                <td>Rs. ${cr[e].paid}</td>
                <td><a href="http://127.0.0.1:8000/inventory/transactions/${dr[e].id}/quickpay/"><span class="badge badge-danger">Pay Rs. ${ cr[e].remaining_payment }</span></a></td>
            </tr>
            `
        cr_table_data += cr_data
        })
    }
    var table = ''
    if (dr_head!=''){
        table+=
            `
            <hr>
            ${dr_head}
            <table id="transactions" class="table table-warning table-sm">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Bought From</th>
                        <th>Item</th>
                        <th>Quantity</th>
                        <th>Total Payable</th>
                        <th>Paid Amount</th>
                        <th>Remaining</th>
                    </tr>
                </thead>
                <tbody>
                    ${dr_table_data}
                </tbody>
            </table>
            `
    }
    if(cr_head!=''){
        table += 
        `
        <hr>
        ${cr_head}
        <table id="transactions" class="table table-danger table-sm">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Sold to</th>
                    <th>Item</th>
                    <th>Quantity</th>
                    <th>Total Payable</th>
                    <th>Paid Amount</th>
                    <th>Remaining</th>
                </tr>
            </thead>
            <tbody>
                ${cr_table_data}
            </tbody>
        </table>
        `
    }
    html = `
        <div class="card">
            <div class="card-header">
                Product Info: ${data.id} - ${data.name}
            </div>
            <div class="card-body">
                <h5 class="card-title">Product Name: <span class='text-secondary'>${data.name}</span></h5><hr>
                <h6 class="">Brand: <span class='text-secondary'>${data.brand}</span></h6>
                <h6 class="">Category: <span class='text-secondary'>${data.category}</span></h6>
                <h6>Cost Price: <span class='text-secondary'>Rs. ${data.cost_price}</span></h6>
                <h6>Product Selling Price: <span class='text-secondary'>Rs. ${data.selling_price}</span></h6>
                <h6>Remaining Quantity: <span class='text-secondary'>${data.quantity}</span></h6>
            </div>
        ${table}
        </div>
    `
    const transInfo = $(".trans-info")
    if (transInfo.length>0){
        transInfo.html(html);
        $("#id_cost").val(data.selling_price);
    }else{
        $("#content-main").html(html)
        $("#myModal").modal();
    }
};

function get_item_info_trans(id){
    var item_id = id
    var url = `http://${window.location.host}/inventory/item/${item_id}/`
    $.ajax({
        url: url,
        method : "GET",
        data:{},
        success: handleResponse,
        error: function(error){
            console.log(error)
        }
    });
};