

$(document).ready(function() {

    function buildTable(selector, data1, data2, data3, data4, data5) {
        const element = $(selector) 
        let content = `
        <table class="table" id="history">
        <thead>
          <tr>
            <th>Customer Name</th>
            <th>User Name</th>
            <th>Creation Date</th>
            <th>PO Date</th>
          </tr>
        </thead>
        <tbody></tbody>
        `


    }

    $('#history_review').click(function() {
        // var formData = new FormData();
        $.ajax({
            url: '/history',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response)  {
                let { customer_names, users, creation_dates, PO_dates } = response
                console.log("___________")
                console.log(customer_names, "customernames")
                console.log(users, "users")
                console.log(creation_dates, "creation_dates")
                console.log(PO_dates, "PO_dates")
                buildTable("#history", customer_names, users, creation_dates, PO_dates)
            }
        })
    })
})