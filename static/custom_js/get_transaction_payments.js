function get_trans_payments(e, trans_id){
    var url = `${window.location.protocol}//${window.location.host}/inventory/transaction/${trans_id}`
    $.ajax({
        url: url,
        method : "GET",
        data:{},
        success: function(data){
            var html = `
            <div class="card">
                <div class="card-header">
                    Transaction ID: ${trans_id} - ${data.item}
                </div>
                <div class="card-body">
                    <h5 class="card-title">Payment For Item: ${data.item}</h5><hr>
                    <h6>Date of Transaction: <span class='text-secondary'>${data.date}<span></h6>
                    <h6>Vendor/ Client Name: <span class='text-secondary'>${data.vendor_client}<span></h6>
                    <h6>Quantity: <span class='badge badge-success'>${data.quantity} Units</span></h6>
                    <h6>Total Payable: <span class='text-warning'>Rs. ${data.payable}</span></h6>
                    <h6>Total Paid: <span class='text-success'>Rs. ${data.paid}</span></h6>
                    <h6>Payment Remaining: <span class='text-danger'>Rs. ${data.remaining_payment}</span></h6>
                    <h6 class="card-text"></h6>
                </div>
            </div>
            `
            $(".trans-info").html(html)
        },
        error: function(error){
            console.log(error)
        }
    });
}