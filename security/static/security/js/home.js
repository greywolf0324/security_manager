/* Bootstrap 5 JS included */

// console.clear();
('use strict');


// Drag and drop - single or multiple image files
// https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
// https://codepen.io/joezimjs/pen/yPWQbd?editors=1000
(function () {

  'use strict';
  
  // Four objects of interest: drop zones, input elements, gallery elements, and the files.
  // dataRefs = {files: [image files], input: element ref, gallery: element ref}

  const preventDefaults = event => {
    event.preventDefault();
    event.stopPropagation();
  };

  const highlight = event =>
    event.target.classList.add('highlight');
  
  const unhighlight = event =>
    event.target.classList.remove('highlight');

  const getInputAndGalleryRefs = element => {
    const zone = element.closest('.upload_dropZone') || false;
    const gallery = zone.querySelector('.upload_gallery') || false;
    const input = zone.querySelector('input[type="file"]') || false;
    return {input: input, gallery: gallery};
  }

  const handleDrop = event => {
    const dataRefs = getInputAndGalleryRefs(event.target);
    dataRefs.files = event.dataTransfer.files;
    handleFiles(dataRefs);
  }


  const eventHandlers = zone => {

    const dataRefs = getInputAndGalleryRefs(zone);
    if (!dataRefs.input) return;

    // Prevent default drag behaviors
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
      zone.addEventListener(event, preventDefaults, false);
      document.body.addEventListener(event, preventDefaults, false);
    });

    // Highlighting drop area when item is dragged over it
    ;['dragenter', 'dragover'].forEach(event => {
      zone.addEventListener(event, highlight, false);
    });
    ;['dragleave', 'drop'].forEach(event => {
      zone.addEventListener(event, unhighlight, false);
    });

    // Handle dropped files
    zone.addEventListener('drop', handleDrop, false);

    // Handle browse selected files
    dataRefs.input.addEventListener('change', event => {
      dataRefs.files = event.target.files;
      handleFiles(dataRefs);
    }, false);

  }


  // Initialise ALL dropzones
  const dropZones = document.querySelectorAll('.upload_dropZone');
  for (const zone of dropZones) {
    eventHandlers(zone);
  }


  // No 'image/gif' or PDF or webp allowed here, but it's up to your use case.
  // Double checks the input "accept" attribute
  const isImageFile = file => 
    ['image/jpeg', 'image/png', 'image/svg+xml'].includes(file.type);


  function previewFiles(dataRefs) {
    if (!dataRefs.gallery) return;
    for (const file of dataRefs.files) {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = function() {
        let img = document.createElement('div');
        img.className = 'upload_img mt-2';
        img.setAttribute('alt', file.name);
        img.innerHTML = file.name;
        dataRefs.gallery.appendChild(img);
      }
    }
  }

  // Based on: https://flaviocopes.com/how-to-upload-files-fetch/
  const imageUpload = dataRefs => {

    // Multiple source routes, so double check validity
    // if (!dataRefs.files || !dataRefs.input) return;

    // const url = dataRefs.input.getAttribute('data-post-url');
    // if (!url) return;

    // const name = dataRefs.input.getAttribute('data-post-name');
    // if (!name) return;

    // const formData = new FormData();
    // formData.append(name, dataRefs.files);

    // fetch(url, {
    //   method: 'POST',
    //   body: formData
    // })
    // .then(response => response.json())
    // .then(data => {
    //   if (data.success === true) {
    //     previewFiles(dataRefs);
    //   } else {
    //   }
    // })
    // .catch(error => {
    // });
  }


  // Handle both selected and dropped files
  const handleFiles = dataRefs => {

    let files = [...dataRefs.files];

    // Remove unaccepted file types
    files = files.filter(item => item);

    if (!files.length) return;
    dataRefs.files = files;

    previewFiles(dataRefs);
    imageUpload(dataRefs);
  }

})();

var terms_opt = '';

function getvalue(element){
  terms_opt = element.value
}

const stepper = document.querySelector('#stepper');
const processStepper = new CDB.Stepper(stepper);

const termsOptionsFromOMS = (term) => {
  const options = [' T/T against BL Copy',
   '0 Days',
   '105 Days',
   '120 Days',
   '15 Days',
   '2% 30 Net 31',
   '25% Deposit - 75% Against BOL',
   '30 Days',
   '30% Deposit - 70% Against BOL',
   '30% Deposit - 70% Before Shipment',
   '45 Days',
   '50% Deposit - 50% Net 30 Days',
   '50% Deposit - 50% Upon Goods Pick Up',
   '60 Days',
   '75 Days',
   '90 Days',
   'Letter of Credit']
   console.log(term, "term")
  return `<select class="form-select terms-options w-75 " onchange="getvalue(this)">${options.map(option => `<option value="${option}" ${option ===  term?"selected":""}>${option}</option>`)}</select>`
}

const term_options = [' T/T against BL Copy',
   '0 Days',
   '105 Days',
   '120 Days',
   '15 Days',
   '2% 30 Net 31',
   '25% Deposit - 75% Against BOL',
   '30 Days',
   '30% Deposit - 70% Against BOL',
   '30% Deposit - 70% Before Shipment',
   '45 Days',
   '50% Deposit - 50% Net 30 Days',
   '50% Deposit - 50% Upon Goods Pick Up',
   '60 Days',
   '75 Days',
   '90 Days',
   'Letter of Credit']

   function sortSelect(user_select) {
    console.log(user_select, "++++++")
    var tmpAry = new Array();
    for (var i=0;i<user_select.options.length;i++) {
        tmpAry[i] = new Array();
        tmpAry[i][0] = user_select.options[i].text;
        tmpAry[i][1] = user_select.options[i].value;
    }
    tmpAry.sort();
    console.log(tmpAry, "++_+_+_+_+_+")
    while (user_select.options.length > 0) {
        user_select.options[0] = null;
    }
    console.log(user_select, "!!!!!!!")
    for (var i=0;i<tmpAry.length;i++) {
        var op = new Option(tmpAry[i][0], tmpAry[i][1]);
        user_select.options[i] = op;
    }
    console.log(user_select, "___")
    return;
}
var user_select = document.getElementById("customername")
sortSelect(user_select)
// console.log(user_select.options[1].text, user_select.options[1].value)
// console.log(user_select, "____")
// var user_options = Array.from(user_select.options)
// user_options.forEach(function(option) {
//   user_select.appendChild(option)
// })
   
$(document).ready(function() {
  

  var uomList = document.getElementById("uom-list")
  var inventoryList = document.getElementById("inventory-list")
  var paymentTerm = document.getElementById("payment-term")
  var originalData = "";
  var savedata=""
  let isMatched = false
  $('#sidebarCollapse').on('click', function () {
    $('#sidebarNav').toggleClass('active');
  });

  
    $('#customername').select2({
      dropdownCssClass: 'custom-dropdown',
      // Add other Select2 configuration options as needed
    });

  $("#customername").change(function() {
    if ($(this).val() === "Pepco") $("#currency-selector").show()
    else $("#currency-selector").hide()
  });

  $("#clear-my-files").click(function() {
    $("#upload_image_background").val("")
    $(".upload_gallery").html("")
  })
  
  function generateTable(selectedOption) {
    // Clear the existing table content
    const customernameoptions = customername==="Buc-ee's"?"<select><option>Buc-ee's</option></select>":"<select><option>Pepco - EUR</option><option>Pepco - CNY</option><option>Pepco - USD</option></select>"
    $('#customselect').empty();

    // Generate the table rows based on the selected option
    // Replace this with your own logic to generate the table content
    for (var i = 1; i <= 5; i++) {
      var row = '<tr><td>Row ' + i + '</td></tr>';
      $('#customselect').append(row);
    }
  }

  // Generate the table on page load
  generateTable($('#customselect').val());

  // Generate the table when the select value changes
  $('#customselect').on('change', function() {
    var selectedOption = $(this).val();
    generateTable(selectedOption);
  });

  function customerStyle() {
    const name = $("#customername").val();
    const styles = [
      "Buc-ee's",
      "Family Dollar",
      "Gabe's",
      "Walmart",
      "Big Lots Stores",
      "TARGET",
      "Five Below",
      "Lekia",
      "Meijers",
      "MICHAELS",
      "Fred Meyer",
    ];
    return styles.includes(name)?"Vendor Style":"Buyers Catalog or Stock Keeping #"
  }

  function buildTable(data_header, data_item, selector, single=true) {
    const keys_header = Object.keys(data_header[0])
    const keys_item = Object.keys(data_item[0])
    const element = $(selector)
    const input_len = data_header.length
    let content = '<div class="black-line" style = "width: 100%; height: 7px; background-color: darkslategray;"></div>'
    for (let i = 0; i < input_len; i++) {
      content += '<h4 class="mt-3 mb-2">Header Details</h4>'
      content += '<table class="table table-bordered" bgcolor="pink">'
      content += "<thead><tr>"
      content += keys_header.map(key => `<th>${key}</th>`)
      content += "</tr></thead><tbody>"

      if (single) {
          content += "<tr>"
          content += keys_header.map((key, index) => `<td>${data_header[i][key]}</td>`)
          content += "</tr>"
        // content += "<tr>"
        // content += keys_header.map((key) => `<td>${data_header[i][key]}</td>`)
        // content += "</tr>"
      } else {
          for (let j = 0; j < data_header[i][keys_header[0]].length; j++) {
            content += "<tr>"
            content += keys_header.map((key, index) => `<td>${data_header[i][key][j]}</td>`)
            content += "</tr>"
          }
      }
      content += '</tbody></table>'
      // Showing item details
      content += '<h4 class="mt-3 mb-2">Item Details</h4>'
      content += '<table class="table table-bordered">'
      content += "<thead><tr>"
      content += keys_item.map(key => `<th>${key}</th>`)
      content += "</tr></thead><tbody>"

      if (single) {
        for (let j = 0; j < data_item[i]["Buyers Catalog or Stock Keeping #"].length; j++){
          content += "<tr>"
          content += keys_item.map((key, index) => `<td>${data_item[i][key][j]}</td>`)
          content += "</tr>"
        }
          
        // content += "<tr>"
        // content += keys_item.map((key) => `<td>${data_item[i][key]}</td>`)
        // content += "</tr>"
      } else {
          for (let j = 0; j < data_item[i][keys_item[0]].length; j++) {
            content += "<tr>"
            content += keys_item.map((key, index) => `<td>${data_item[i][key][j]}</td>`)
            content += "</tr>"
          }
      }
      content += '</tbody></table>'
      content += '<div class="black-line" style = "width: 100%; height: 7px; background-color: darkslategray"></div>'
    }
    element.html(content)
    // =======================
    // const keys = Object.keys(data)
    // const elemen = $(selector)
    // let conten = "<thead><tr>"

    // conten += keys.map(key => `<th>${key}</th>`)
    // conten += "</tr></thead><tbody>"

    // if (single) {
    //   conten += "<tr>"
    //   conten += keys.map((key) => `<td>${data[key]}</td>`)
    //   conten += "</tr>"
    // } else {
    //   for (let i = 0; i < data[keys[0]][0].length; i++) {
    //     conten += "<tr>"
    //     conten += keys.map((key, index) => `<td>${data[key][0][i]}</td>`)
    //     conten += "</tr>"
    //   }
    // }
    // element.html(conten)
  }

  function displayTable(data, selector, selector1, options, termRsOptions, data3, locations, data5) {
    const keys = ["Buyers Catalog or Stock Keeping #", "Vendor Style", "Product/Item Description", "Unit of Measure", "StockLocation", "Vendor Style from OMS_equal"]
    console.log(data5, "data5")
    const customername = data5
    const customernameoptions = customername==="Pepco"?"<select class='w-75 form-select'><option>Pepco - EUR</option><option>Pepco - CNY</option><option>Pepco - USD</option></select>":`<select class='w-75 form-select'><option>${customername}</option></select>`
    
    var termsfrompo = data[0]["Payment Terms Net Days"][0]||""
    // if (termsfrompo !== ""){
    //   for (var key in term_options) {
    //     console.log(term_options[key], termsfrompo, "++++++++++++++++++++++++++")
    //     if (term_options[key].includes(termsfrompo)) {
    //       termsfrompo = term_options[key]
    //       break;
    //     }
    //   }  
    // }
    var head1 = `<div class="table table-striped border rounded">
                  <div class="row px-5 py-3">
                    <div class="col-lg-6">
                      <div class="fw-bold">Customer Name From P0: <span class="text-danger">${customername}</span></div>
                    </div>
                    <div class="col-lg-6">
                      <div class="row fw-bold">
                        <div class="col-lg-4 text-start">
                          Customer Name Options: 
                        </div>
                        <div class="col-lg-8">
                          ${customernameoptions}
                        </div>                      
                      </div>                    
                    </div>
                    <div class="col-lg-6">
                      <div class="fw-bold">Terms From PO: <span class="text-danger">${termsfrompo}</span></div>                    
                    </div>
                    <div class="col-lg-6">
                      <div class="row fw-bold">
                        <div class="col-lg-4 text-start">
                          Terms Options From OMS: 
                        </div>
                        <div class="col-lg-8">
                          ${termsOptionsFromOMS(termRsOptions)}
                        </div>                      
                      </div>
                    </div>
                  </div>
                </div>`;
    $(selector1).html(head1)
    console.log(data, "_____")
    const table_len = data.length
    const sku_keyname = customerStyle(customername)
    var tables = `
  
    <thead>
      <tr>
        ${
          keys.map(key => `<th>${key}</th>`)
        }
      </tr>
    </thead><tbody>
    `;
    let temp = {}
    for(var i = 0;i<data.length;i++){
      console.log(data[0], "+++++ ")
      console.log(keys[0], "_____")
      tables += `
    
    
      ${
        [...Array(data[i][keys[0]].length)].map((_, index) => {
          if (temp[data[i][sku_keyname][index]]) return ""
          temp[data[i][sku_keyname][index]] = true
          return index && `   
            <tr >
              ${
                keys.map(key => {
                  if (key === "Vendor Style from OMS_equal") {
                    try {
                      var selectedValue = data3[data[i][sku_keyname][index]][2]
                      var determinevalue = data3[data[i][sku_keyname][index]][2]
                  }
                    catch{
                      var selectedValue = data3[data[i][sku_keyname][index]]
                      var determinevalue = data3[data[i][sku_keyname][index]]
                    }
                    const hasValue = options["sku_options"][i][index - 1].findIndex(v => v==selectedValue) !== -1
                    return `<td contenteditable="true"><select class="form-select" ${hasValue?"disabled":""} data-hasvalue="${hasValue}"><option value="" disabled selected>Select Vendor Style</option>${options["sku_options"][i][index - 1].map(option => `<option value="${option}" ${option==selectedValue?"selected":""}>${option}</option>`)}</select></td>`;
                  }
                  else if (key === "Unit of Measure") {
                    try {
                      var selectedValue = data3[data[i][sku_keyname][index]][0]
                      var determinevalue = data3[data[i][sku_keyname][index]][2]
                    }
                    catch{
                      var selectedValue = data3[data[i][sku_keyname][index]]
                      var determinevalue = data3[data[i][sku_keyname][index]]
                    }
                    const hasValue = options["sku_options"][i][index - 1].findIndex(v => v==determinevalue) !== -1
                    return `<td contenteditable="true"><select class="form-select" ${hasValue?"disabled":""} data-hasvalue="${hasValue}"><option value="" disabled selected>Select UOM</option>${options["uom_options"][i][index - 1].map(option => `<option value="${option}" ${option==selectedValue?"selected":""}>${option}</option>`)}</select></td>`;
                  }
                  else if (key === "StockLocation") {
                    try {
                      var selectedValue = data3[data[i][sku_keyname][index]][1]
                      var determinevalue = data3[data[i][sku_keyname][index]][2]
                  }
                    catch{
                      var selectedValue = data3[data[i][sku_keyname][index]]
                      var determinevalue = data3[data[i][sku_keyname][index]]
                    }
                    const hasValue = options["sku_options"][i][index - 1].findIndex(v => v==determinevalue) !== -1
                    return `<td contenteditable="true"><select class="form-select" ${hasValue?"disabled":""} data-hasvalue="${hasValue}"><option value="" disabled selected>Select StockLocation</option>${options["location_options"][i][index - 1].map(option => `<option value="${option}" ${option==selectedValue?"selected":""}>${option}</option>`)}</select></td>`;
                  }
                  return `<td contenteditable="true">${data[i][key][index]}</td>`;
                })
              }
            </tr>`
        })
      }
  `
    }
    tables += '</tbody>'
    $(selector).html(tables)
    $(selector).parent().removeClass('d-none')
  }

  function getTableData(selector) {
    var tableData = {};
    const keys = ["Buyers Catalog or Stock Keeping #", "Vendor Style", "Product/Item Description", "Unit of Measure", "StockLocation", "Vendor Style from OMS_equal"]
    let hasValue = []

    $(`${selector} tbody tr`).each(function() {
      $(this).find('td').each(function(columnIndex, cell) {
        var headerText = keys[columnIndex];
        let value = $(cell).text()
        if (headerText === "Vendor Style from OMS_equal") {
          value = cell.children[0]?.value
          hasValue.push(cell.children[0]?.getAttribute("data-hasvalue"))
          if (!value) value = ""
          headerText = "Vendor Style from OMS_equal"
        }
        if (headerText === "Unit of Measure") {
          value = cell.children[0]?.value
          if (!value) value = ""
        }
        if (headerText === "StockLocation") {
          value = cell.children[0]?.value
          if (!value) value = ""
        }
        if (!tableData[headerText]) tableData[headerText] = []
        tableData[headerText].push(value);
      });
    });
    return [tableData, hasValue]
  }

  $("#savebutton").click(function() {
    // const [customInputs] = getTableData("#table-view")
  })
  $("#first-step-next").click(function() {
    var formData = new FormData($('#data-form')[0]);
    document.getElementById('loader1').classList.toggle('d-none');
    $.ajax({
      url: '/parse-upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        let { data1, data2, data3, data4, data5 } = response
        console.log(data1, "_____")
        data1 = JSON.parse(data1)
        data2 = JSON.parse(data2)
        data3 = JSON.parse(data3)
        data4 = JSON.parse(data4)
        data5 = JSON.parse(data5)
        originalData = data1
        savedata= data3
        len = data2.OMS_Inventory_List.length
        uom = ["Each", "Case"]
        locat = ["FOB", "Houston Warehouse", "MFAL", "Arrow Mill"]
        uoms = []
        locations = []

        for (let i = 0; i < data2.OMS_Inventory_List.length; i++) {
          uoms.push([])
          locations.push([])
          for (let j = 0; j < data2.OMS_Inventory_List[i].length; j++){
            uoms[i].push(uom)
            locations[i].push(locat)
          }
          
        }
        displayTable(data1, "#table-view", "#table-header-view", {"sku_options": data2.OMS_Inventory_List, "uom_options": uoms, "location_options": locations}, data2.OMS_Payment_term, data3, data4, data5)
        document.getElementById('loader1').classList.toggle('d-none');
      },
      error: function(xhr, status, error) {
          $('#message').text('Error uploading files: ' + error);
      }
    });
  })
  $("#openDialogButton").click(function() {
    
    data=savedata
    inputdata=getTableData("#table-view")
    const customername = $("#customername").val();
    const keyname = customerStyle(customername)
    const [inputs, hasValue] = inputdata
    var table = '<table>'
    var newtable = '<table>'
   
    table += `<thead><tr><th>${keyname}</th><th>Unit of Measure</th><th>StockLocation</th><th>Vendor Style from OMS_equal</th></tr></thead>`;
    table += '<tbody>';
    newtable += `<thead><tr><th>${keyname}</th><th>Unit of Measure</th><th>StockLocation</th><th>Vendor Style from OMS_equal</th><th></th><th></th></tr></thead>`;
    newtable += '<tbody>';
    
    hasValue.forEach(function(v, index) {
      const key = inputs[keyname][index]
      const value1 = inputs["Unit of Measure"][index]
      const value2 = inputs["StockLocation"][index]
      const value3 = inputs["Vendor Style from OMS_equal"][index]
      if (v === 'true')
        table += '<tr><td>' + key + '</td><td>' + value1 + '</td><td>' + value2 + '</td><td>' + value3 + '</td></tr>';
      else
        newtable += '<tr><td>' + key + '</td><td>' + value1 + '</td><td>' + value2 + '</td><td>' + value3 + '</td></tr>';
    })
    

    table += '</tbody></table>';
    newtable += '</tbody></table>';
    $("#modaltable").html(table)
    $("#newmodaltable").html(newtable)
    
  });
  $("#openDialogButton").click(function(event) {
    openDialog();
  });

  function openDialog() {
      $("#myModal").modal("show");
  }
  function closeDialog() {
    // Perform actions to close the dialog
    $("#myModal").modal("hide");
  }

  function buildFinalForm() { 
    var formData = new FormData($('#data-form')[0]);
    const keyname = customerStyle()
    const [customInputs] = getTableData("#table-view")

    for (const customer of customInputs["Vendor Style from OMS_equal"]) {
      if (customer === "") {
        toastr.error("Fill Every Vendor Style", 'Error');
        return
      }
    }
    const clonedArray = JSON.parse(JSON.stringify(originalData))

    originalData.forEach(data => {      
      const customerHeader = [...data[keyname]];
      data["Vendor Style"] = data[keyname].map((vs,index) => {
        const idx = customInputs[keyname].findIndex(v => v == vs)
        return index?customInputs["Vendor Style from OMS_equal"][idx]:""
      })

      data["Unit of Measure"] = customerHeader.map((vs,index) => {
        const idx = customInputs[keyname].findIndex(v => v == vs)
        return index?customInputs["Unit of Measure"][idx]:""
      })
      data["StockLocation"] = customerHeader.map((vs,index) => {
        const idx = customInputs[keyname].findIndex(v => v == vs)
        return index?customInputs["StockLocation"][idx]:""
      })
    })

    formData.append("input", JSON.stringify(originalData))
    var termsOptions = ''

    if (terms_opt != ''){
      termsOptions = $(".terms-options").map(function() {
        return $(this).val();
      }).get();
    }
    else{
      termsOptions = [$("#default-terms").text()]
    }
    // termsOptions = $(".terms-options").map(function() {
    //   return $(this).val();
    // }).get();

    formData.append("termOptions", JSON.stringify(termsOptions))
    originalData = clonedArray
    
    return formData
  }

  



  $('#NextButton').click(function() {
    const formData = buildFinalForm()
    processStepper.navigate('3')
    closeDialog()
    document.getElementById('loader2').classList.toggle('d-none');
    $.ajax({
      url: '/viewer',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        const [_customername, headerDetails, itemDetails] = JSON.parse(response.res)
        $(".review-stepper .customername").html(_customername);
        buildTable(headerDetails, itemDetails, "#view_details")
        document.getElementById('loader2').classList.toggle('d-none');
        // buildTable(itemDetails[0], "#item-details")
        // buildTable(headerDetails[0], "#header-details", true)
      },
      error: function(xhr, status, error) {
      }
    })
  });

  $('#final-step').click(function() {
    const formData = buildFinalForm()
    document.getElementById('csv-container').classList.toggle('d-none');
    document.getElementById('loader3').classList.toggle('d-none');
    $.ajax({
      url: '/',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $("#download-output").attr('href', `/download-file/${response.id}`)
        document.getElementById('csv-container').classList.toggle('d-none');
        document.getElementById('csv-container').innerHTML = `<h5 class="text-success">Click Download button to download your result</h5>`;
        document.getElementById('loader3').classList.toggle('d-none');
      },
      error: function(xhr, status, error) {
        if (xhr.status === 400) {
          document.getElementById('csv-container').classList.toggle('d-none');
          document.getElementById('csv-container').innerHTML = `<h5 class="text-danger">Database is not enough</h5>`
          document.getElementById('loader3').classList.toggle('d-none');
        }
      }
    })
  });

  function openliveDialog() {
    $("#liveModal").modal("show");
  }
  function closeliveDialog() {
    // Perform actions to close the dialog
    $("#liveModal").modal("hide");
  }
  
  $('#sheet-exporter').click(function() {
    
    // document.getElementById('csv-container').classList.toggle('d-none');
    // document.getElementById('loader2').classList.toggle('d-none');
    openliveDialog();
    // window.open("/export-file")
  });
  $('#liveAccept').click(function() {
    const formData = buildFinalForm()
    $.ajax({
      url: '/export-doubleUpdate',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {

      },
      error: function(xhr, status, error) {
        if (xhr.status === 400) {
          document.getElementById('csv-container').classList.toggle('d-none');
          document.getElementById('csv-container').innerHTML = `<h5 class="text-danger">Database is not enough</h5>`
          document.getElementById('loader2').classList.toggle('d-none');
        }
      }
    })

  })

  // $('#liveIgnore').click(function() {
  //   closeliveDialog()
  // })

  $('#liveIgnore').click(function() {
    const formData = buildFinalForm()
    $.ajax({
      url: '/export-doubleIgnore',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {

      },
      error: function(xhr, status, error) {
        if (xhr.status === 400) {
          document.getElementById('csv-container').classList.toggle('d-none');
          document.getElementById('csv-container').innerHTML = `<h5 class="text-danger">Database is not enough</h5>`
          document.getElementById('loader2').classList.toggle('d-none');
        }
      }
    })
  })

  // $('#history_viewer').addEventListener('click', function(event) {
  //   event.preventDefault();

  //   var xhr = new XMLHttpRequest();
  //   xhr.open('GET', '/responser/', true);
  //   xhr.onreadystatechange = function() {
  //       if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
  //           // Handle the response here
  //           var response = JSON.parse(xhr.responseText);
  //           console.log(response, "_____+++++"); // Access the received data
  //       }
  //   };
  //   xhr.send();
  // })
});