function handleResponse(data){
    var html = ''
    var dr = data.unpaid_dr_trans
    var cr = data.unpaid_cr_trans
    var dr_table_data = ''
    var cr_table_data = ''
    if (dr.length >0){
        var dr_head = '<h4>Stock In Unpaid Transactions</h4>'
        $.each(dr, function(e){
            var dr_data = 
            `
            <tr>
                <td>${dr[e].date}</td>
                <td>${dr[e].vendor_client}</td>
                <td><a href="#">${dr[e].item}</a></td>
                <td>${dr[e].quantity}</td>
                <td>Rs. ${dr[e].payable}</td>
                <td>Rs. ${dr[e].paid}</td>
                <td><span class="badge badge-warning">Rs. ${ dr[e].remaining_payment }</span></td>
            </tr>
            `
        dr_table_data += dr_data
        })
    }
    if (cr.length >0){
        var cr_head = '<h4>Stock Out Unpaid Transactions</h4>'
        $.each(cr, function(e){
            var cr_data = 
            `
            <tr>
                <td>${cr[e].date}</td>
                
                <td>${cr[e].vendor_client}</td>
                <td><a href="#">${cr[e].item}</a></td>
                <td>${cr[e].quantity}</td>
                <td>Rs. ${cr[e].payable}</td>
                <td>Rs. ${cr[e].paid}</td>
                <td><span class="badge badge-danger">Rs. ${ cr[e].remaining_payment }</span></td>
            </tr>
            `
        cr_table_data += cr_data
        })
    }
    var table = 
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
    if(cr_head){
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
    $("#content-main").html(html)
    $(".trans-info").html(html);
    $("#id_cost").val(data.selling_price);
    $("#myModal").modal();
};

function get_item_info_trans(e, id){
    e.preventDefault();
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