/* Bootstrap 5 JS included */

console.clear();
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
    //   console.log('posted: ', data);
    //   if (data.success === true) {
    //     previewFiles(dataRefs);
    //   } else {
    //     console.log('URL: ', url, '  name: ', name)
    //   }
    // })
    // .catch(error => {
    //   console.error('errored: ', error);
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

const stepper = document.querySelector('#stepper');
const processStepper = new CDB.Stepper(stepper);

$(document).ready(function() {

  var uomList = document.getElementById("uom-list")
  var inventoryList = document.getElementById("inventory-list")
  var paymentTerm = document.getElementById("payment-term")

  $("#customername").change(function() {
    if ($(this).val() === "Pepco") $("#currency-selector").show()
    else $("#currency-selector").hide()
  });

  function displayTable(data, selector) {
    const keys = Object.keys(data)
    $(selector).html(`
      <thead>
        <tr>
          ${keys.map(key => `<th>${key}</th>`)}
        </tr>
      </thead>
      <tbody>
        ${
          [...Array(data[keys[0]].length)].map((_, index) => `
            <tr>
              ${
                keys.map(key => `<td contenteditable="true">${data[key][index]}</td>`)
              }
            </tr>
          `)
        }
      </tbody>
    `)
  }

  function checkVendorStyle(selector) {
    let isValid = true
    $(`${selector} tbody tr`).each(function() {
      $(this).find('td').each(function(columnIndex, cell) {
        var headerText = $(`${selector} thead th`).eq(columnIndex).text();
        if (headerText === "Vendor Style" && $(cell).text() === "") {
          isValid = false
          return
        }
      });
      if (!isValid) return
    });
    return isValid
  }

  function getTableData(selector) {
    var tableData = {};
    $(`${selector} tbody tr`).each(function() {
      $(this).find('td').each(function(columnIndex, cell) {
        var headerText = $(`${selector} thead th`).eq(columnIndex).text();
        if (headerText === "Vendor Style" && $(cell).text() === "") {
          alert("You have to fill vendor style for every row")
          return
        }
        if (!tableData[headerText]) tableData[headerText] = []
        tableData[headerText].push($(cell).text());
      });
    });
    return JSON.stringify([tableData])
  }

  $("#first-step-next").click(function() {
    var formData = new FormData($('#data-form')[0]);
    $.ajax({
      url: '/parse-upload',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        let { data1, data2 } = response
        data1 = JSON.parse(data1)[0]
        data2 = JSON.parse(data2)
        data2_uom = data2.OMS_AdditionalUOM[0]
        data2_inventory = data2.OMS_InventoryList[0]

        displayTable(data1, "#table-view")
        displayTable(data2_uom, "#additional-uom-table")
        displayTable(data2_inventory, "#inventory-list-table")
      },
      error: function(xhr, status, error) {
          $('#message').text('Error uploading files: ' + error);
      }
    });
  })

  $("#second-step-next").click(function() {
    if (!checkVendorStyle()) {
      alert("Please fill for vendor style for each row!")
      return
    }
    var formData = new FormData();
    formData.append("input", getTableData("#table-view"))
    formData.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    $.ajax({
      url: '/required-items',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {

        const { fields } = response

        let uomListHTML = ""
        for (const uom of fields[0]) {
          if (!uom) continue
          uomListHTML += `
            <div class="mt-3 border rounded p-3" id="uom-${uom}">
              <h5>SKU - ${uom}</h5>
              <div>
                <label class="form-label">Action</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Base SKU</label>
                <input type="text" class="form-control" readonly value="${uom}" />
              </div>
              <div>
                <label class="form-label">Base Product Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Base Unit Of Measure</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Additional Units Of Measure SKU</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Additional Units Of Measure ProductName</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Additional Units Of Measure Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Number Of Base Units In Additional Unit</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">I Am Selling This Product</label>
                <input type="text" class="form-control" />
              </div>
            </div>
          `
        }
        uomList.innerHTML = uomListHTML

        let inventoryListHTML = ""
        for (const inventory of fields[2]) {
          if (!inventory) continue
          inventoryListHTML += `
            <div class="mt-3 border rounded p-3" id="inventory-${inventory}">
              <h5>SKU - ${inventory}</h5>
              <div>
                <label class="form-label">Product Code</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Category</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Brand</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Type</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">FixedAssetType</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CostingMethod</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Length</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Width</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Height</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Weight</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonLength</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonWidth</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonHeight</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonInnerQuantity</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonQuantity</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CartonVolume</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">WeightUnits</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionUnits</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Barcode</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">MinimumBeforeReorder</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ReorderQuantity</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DefaultLocation</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">LastSuppliedBy</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">SupplierProductCode</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">SupplierProductName</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">SupplierFixedPrice</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier1</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier2</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier3</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier4</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier5</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier6</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier7</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier8</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier9</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PriceTier10</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AssemblyBOM</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AutoAssemble</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AutoDisassemble</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DropShip</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DropShipSupplier</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AverageCost</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DefaultUnitOfMeasure</label>
                <input type="text" class="form-control" />
              </div>

              <div>
                <label class="form-label">InventoryAccount</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">RevenueAccount</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ExpenseAccount</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">COGSAccount</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductAttributeSet</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute1</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute2</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute3</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute4</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute5</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute6</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute7</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute8</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute9</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AdditionalAttribute10</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DiscountName</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilySKU</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyName</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyOption1Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyOption1Value</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyOption2Name</label>
                <input type="text" class="form-control" />
              </div>

              <div>
                <label class="form-label">ProductFamilyOption2Value</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyOption3Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductFamilyOption3Value</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CommaDelimitedTags</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">StockLocator</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PurchaseTaxRule</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">SaleTaxRule</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Status</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Description</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ShortDescription</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Sellable</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PickZones</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">AlwaysShowQuantity</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">WarrantySetupName</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">InternalNote</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">ProductionBOM</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">MakeToOrderBom</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">QuantityToProduce</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">IsAccountingDimensionEnabled</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute1</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute2</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute3</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute4</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute5</label>
                <input type="text" class="form-control" />
              </div>

              <div>
                <label class="form-label">DimensionAttribute6</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute7</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute8</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute9</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DimensionAttribute10</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">HSCode</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">CountryOfOrigin</label>
                <input type="text" class="form-control" />
              </div>
            </div>
          `
        }
        inventoryList.innerHTML = inventoryListHTML

        if (fields[1].length && fields[1][0] !== "") {
          const id = fields[1][0]
          paymentTerm.innerHTML = `
            <div class="mt-3 border rounded p-3" id="payment-term-${id}">
              <h5>${id}</h5>
              <div>
                <label class="form-label">Name</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Days</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">Method</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">DueNextMonth</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PaymentTermActive</label>
                <input type="text" class="form-control" />
              </div>
              <div>
                <label class="form-label">PaymentTermDefault</label>
                <input type="text" class="form-control" />
              </div>
            </div>
          `
        }
      },
      error: function(xhr, status, error) {
          $('#message').text('Error uploading files: ' + error);
      }
    });
  })

  $('#form-submit').click(function() {
      var formData = new FormData($('#data-form')[0]);
      formData.append("input", getTableData("#table-view"))
      document.getElementById('csv-container').classList.toggle('d-none');
      document.getElementById('loader').classList.toggle('d-none');

      //collect additional uoms
      let uoms = []
      let inventories = []
      let paymentTerms = []
      for (let i = 0; i < uomList.children.length; i++) {
        const uom = uomList.children[i]
        const sku = uom.id.replace("uom-", "")
        let _uom = []

        for (let j = 1; j < uom.children.length; j++) {
          _uom.push(uom.children[j].children[1].value)
        }
        uoms.push(_uom)
      }

      for (let i = 0; i < inventoryList.children.length; i++) {
        const inventory = inventoryList.children[i]
        const sku = inventory.id.replace("inventory-", "")
        let _inventory = []

        for (let j = 1; j < inventory.children.length; j++) {
          _inventory.push(inventory.children[j].children[1].value)
        }
        inventories.push(_inventory)
      }

      formData.append("additions", JSON.stringify([uoms, [], inventories  ]))

      $.ajax({
          url: '/',
          type: 'POST',
          data: formData,
          processData: false,
          contentType: false,
          success: function(response) {
            $("#download-output").attr('href', `/download-file/${response.id}`)
            $.get(`/download-file/${response.id}`, function (xlsxData) {
              var workbook = XLSX.read(xlsxData, { type: 'array' });
            
              // Access the first sheet
              var sheetName = workbook.SheetNames[0];
              var sheet = workbook.Sheets[sheetName];
            
              // Convert sheet data to JSON
              var jsonData = XLSX.utils.sheet_to_json(sheet, { header: 1 });
            
              // Generate HTML table
              var tableHtml = '<table class="table table-striped table-bordered">';
              for (var i = 0; i < jsonData.length; i++) {
                tableHtml += '<tr>';
                for (var j = 0; j < jsonData[i].length; j++) {
                  tableHtml += '<td>' + jsonData[i][j] + '</td>';
                }
                tableHtml += '</tr>';
              }
              tableHtml += '</table>';
              
              document.getElementById('csv-container').classList.toggle('d-none');
              document.getElementById('loader').classList.toggle('d-none');            
              // Display the table in the HTML container
              $('#xlsx-container').html(tableHtml);
            })
            .fail(function(error) {
              console.error('Error fetching CSV file:', error);
            });
          },
          error: function(xhr, status, error) {
              $('#message').text('Error uploading files: ' + error);
          }
      });
  });
});