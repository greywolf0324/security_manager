// if (!checkVendorStyle("#table-view")) {
    //   alert("Please fill for vendor style for each row!")
    // } else {
    //   var formData = new FormData();
    //   formData.append("input", getTableData("#table-view"))
    //   formData.append("csrfmiddlewaretoken", $("input[name='csrfmiddlewaretoken']").val())
    //   $.ajax({
    //     url: '/required-items',
    //     type: 'POST',
    //     data: formData,
    //     processData: false,
    //     contentType: false,
    //     success: function(response) {

    //       const { fields } = response

    //       let uomListHTML = ""
    //       for (const uom of fields[0]) {
    //         if (!uom) continue
    //         uomListHTML += `
    //           <div class="mt-3 border rounded p-3" id="uom-${uom}">
    //             <h5>SKU - ${uom}</h5>
    //             <div>
    //               <label class="form-label">Action</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Base SKU</label>
    //               <input type="text" class="form-control" readonly value="${uom}" />
    //             </div>
    //             <div>
    //               <label class="form-label">Base Product Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Base Unit Of Measure</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Additional Units Of Measure SKU</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Additional Units Of Measure ProductName</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Additional Units Of Measure Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Number Of Base Units In Additional Unit</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">I Am Selling This Product</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //           </div>
    //         `
    //       }
    //       uomList.innerHTML = uomListHTML

    //       let inventoryListHTML = ""
    //       for (const inventory of fields[2]) {
    //         if (!inventory) continue
    //         inventoryListHTML += `
    //           <div class="mt-3 border rounded p-3" id="inventory-${inventory}">
    //             <h5>SKU - ${inventory}</h5>
    //             <div>
    //               <label class="form-label">Product Code</label>
    //               <input type="text" class="form-control" readonly value="${inventory}" />
    //             </div>
    //             <div>
    //               <label class="form-label">Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Category</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Brand</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Type</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">FixedAssetType</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CostingMethod</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Length</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Width</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Height</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Weight</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonLength</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonWidth</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonHeight</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonInnerQuantity</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonQuantity</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CartonVolume</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">WeightUnits</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionUnits</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Barcode</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">MinimumBeforeReorder</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ReorderQuantity</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DefaultLocation</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">LastSuppliedBy</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">SupplierProductCode</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">SupplierProductName</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">SupplierFixedPrice</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier1</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier2</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier3</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier4</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier5</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier6</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier7</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier8</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier9</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PriceTier10</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AssemblyBOM</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AutoAssemble</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AutoDisassemble</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DropShip</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DropShipSupplier</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AverageCost</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DefaultUnitOfMeasure</label>
    //               <input type="text" class="form-control" />
    //             </div>

    //             <div>
    //               <label class="form-label">InventoryAccount</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">RevenueAccount</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ExpenseAccount</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">COGSAccount</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductAttributeSet</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute1</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute2</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute3</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute4</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute5</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute6</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute7</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute8</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute9</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AdditionalAttribute10</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DiscountName</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilySKU</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyName</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyOption1Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyOption1Value</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyOption2Name</label>
    //               <input type="text" class="form-control" />
    //             </div>

    //             <div>
    //               <label class="form-label">ProductFamilyOption2Value</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyOption3Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductFamilyOption3Value</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CommaDelimitedTags</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">StockLocator</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PurchaseTaxRule</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">SaleTaxRule</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Status</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Description</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ShortDescription</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Sellable</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PickZones</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">AlwaysShowQuantity</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">WarrantySetupName</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">InternalNote</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">ProductionBOM</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">MakeToOrderBom</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">QuantityToProduce</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">IsAccountingDimensionEnabled</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute1</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute2</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute3</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute4</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute5</label>
    //               <input type="text" class="form-control" />
    //             </div>

    //             <div>
    //               <label class="form-label">DimensionAttribute6</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute7</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute8</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute9</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DimensionAttribute10</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">HSCode</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">CountryOfOrigin</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //           </div>
    //         `
    //       }
    //       inventoryList.innerHTML = inventoryListHTML

    //       if (fields[1].length && fields[1][0] !== "") {
    //         const id = fields[1][0]
    //         paymentTerm.innerHTML = `
    //           <div class="mt-3 border rounded p-3" id="payment-term-${id}">
    //             <h5>${id}</h5>
    //             <div>
    //               <label class="form-label">Name</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Days</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">Method</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">DueNextMonth</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PaymentTermActive</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //             <div>
    //               <label class="form-label">PaymentTermDefault</label>
    //               <input type="text" class="form-control" />
    //             </div>
    //           </div>
    //         `
    //       }
    //     },
    //     error: function(xhr, status, error) {
    //         $('#message').text('Error uploading files: ' + error);
    //     }
    //   });
    //   processStepper.navigate('3')
    // }

    //collect additional uoms
      // let uoms = []
      // let inventories = []
      // let paymentTerms = []
      // for (let i = 0; i < uomList.children.length; i++) {
      //   const uom = uomList.children[i]
      //   const sku = uom.id.replace("uom-", "")
      //   let _uom = []

      //   for (let j = 1; j < uom.children.length; j++) {
      //     _uom.push(uom.children[j].children[1].value)
      //   }
      //   uoms.push(_uom)
      // }

      // for (let i = 0; i < inventoryList.children.length; i++) {
      //   const inventory = inventoryList.children[i]
      //   const sku = inventory.id.replace("inventory-", "")
      //   let _inventory = []

      //   for (let j = 1; j < inventory.children.length; j++) {
      //     _inventory.push(inventory.children[j].children[1].value)
      //   }
      //   inventories.push(_inventory)
      // }

      // formData.append("additions", JSON.stringify([uoms, [], inventories  ]))