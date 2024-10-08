from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


User = get_user_model()

class Customers(models.Model):
  customer_name = models.CharField(max_length = 30)
  sku_bl = models.BooleanField(null=True)

class Matching_dict(models.Model):
  customer_name = models.CharField(max_length = 30)
  parser = models.CharField(max_length = 30)
  matcher = models.CharField(max_length = 30)

class Osalesimport_fields(models.Model):
  field_name = models.CharField(max_length = 50)

class ProcessHistory(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  input = models.CharField(max_length=1000, null=True)
  output = models.CharField(max_length=1000, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
class Original_SalesImport(models.Model):
  start_line = models.BooleanField(default = False)
  approved = models.BooleanField(default = False)
  created = models.CharField(max_length = 1000, null = True)
  PO_Number = models.CharField(max_length = 50, null = True)
  Release_Number = models.CharField(max_length = 50, null = True)
  PO_Date = models.DateField(null = True)
  Dept = models.CharField(max_length = 1000, null = True)
  Retailers_PO = models.CharField(max_length = 1000, null = True)
  Requested_Delivery_Date = models.DateField(null = True)
  Delivery_Dates = models.DateField(null = True)
  Ship_Dates = models.DateField(null = True)
  Cancel_Date = models.DateField(null = True)
  Carrier = models.CharField(max_length = 1000, null = True)
  Carrier_Details = models.CharField(max_length = 1000, null = True)
  Ship_To_Location = models.CharField(max_length = 1000, null = True)
  PO_Line = models.CharField(max_length = 1000, null = True)
  Qty_Ordered = models.CharField(max_length = 1000, null = True)
  Unit_of_Measure = models.CharField(max_length = 1000, null = True)
  Unit_Price = models.CharField(max_length = 1000, null = True)#models.DecimalField(decimal_places = 3, null = True, max_digits = 10)
  Buyers_Catalog_or_Stock_Keeping = models.CharField(max_length = 1000, null = True)
  UPC_EAN = models.CharField(max_length = 1000, null = True)
  Vendor_Style = models.CharField(max_length = 1000, null = True)
  Retail_Price = models.CharField(max_length = 1000, null = True)#models.DecimalField(decimal_places = 3, null = True, max_digits = 10)
  Product_Item_Description = models.CharField(max_length = 1000, null = True)
  Color = models.CharField(max_length = 1000, null = True)
  Size = models.CharField(max_length = 1000, null = True)
  Pack_Size = models.CharField(max_length = 1000, null = True)
  Pack_Size_UOM = models.CharField(max_length = 1000, null = True)
  Number_of_Inner_Packs = models.BigIntegerField(null = True)
  Number_of_Pcs_per_Inner_Pack = models.BigIntegerField(null = True)
  Store = models.CharField(max_length = 1000, null = True)
  Qty_per_Store = models.BigIntegerField(null = True)
  Record_Type = models.CharField(max_length = 1000, null = True)
  PO_purpose = models.CharField(max_length = 1000, null = True)
  PO_Type = models.CharField(max_length = 1000, null = True)
  Contract_Number = models.CharField(max_length = 1000, null = True)
  Currency = models.CharField(max_length = 1000, null = True)
  Ship_Status = models.CharField(max_length = 1000, null = True)
  Letter_of_Credit = models.CharField(max_length = 1000, null = True)
  Vendor = models.CharField(max_length = 1000, null = True)
  Division = models.CharField(max_length = 1000, null = True)
  Cust_Acct = models.CharField(max_length = 1000, null = True)
  Customer_Order = models.CharField(max_length = 1000, null = True)
  Promo = models.CharField(max_length = 1000, null = True)
  Ticket_Description = models.CharField(max_length = 1000, null = True)
  Other_Info = models.CharField(max_length = 1000, null = True)
  Frt_Terms = models.CharField(max_length = 1000, null = True)
  Carrier_Service_Level = models.CharField(max_length = 1000, null = True)
  Payment_Terms = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Disc_Due_Date = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Disc_Days_Due = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Net_Due_Date = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Net_Days = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Disc_Amt = models.CharField(max_length = 1000, null = True)
  Payment_Terms_Desc = models.CharField(max_length = 1000, null = True)
  Contact_Phone = models.CharField(max_length = 1000, null = True)
  Contact_Fax = models.CharField(max_length = 1000, null = True)
  Contact_Email = models.CharField(max_length = 1000, null = True)
  AllowCharge_Type = models.CharField(max_length = 1000, null = True)
  AllowCharge_Service = models.CharField(max_length = 1000, null = True)
  AllowCharge_Amt = models.CharField(max_length = 1000, null = True)
  AllowCharge = models.CharField(max_length = 1000, null = True)
  AllowCharge_Rate = models.CharField(max_length = 1000, null = True)
  AllowCharge_Qty = models.CharField(max_length = 1000, null = True)
  AllowCharge_Desc = models.CharField(max_length = 1000, null = True)
  Ship_To_Name = models.CharField(max_length = 1000, null = True)
  Ship_To_Address_1 = models.CharField(max_length = 1000, null = True)
  Ship_To_Address_2 = models.CharField(max_length = 1000, null = True)
  Ship_To_City = models.CharField(max_length = 1000, null = True)
  Ship_To_State = models.CharField(max_length = 1000, null = True)
  Ship_to_Zip = models.CharField(max_length = 1000, null = True)
  Ship_To_Country = models.CharField(max_length = 1000, null = True)
  Ship_To_Contact = models.CharField(max_length = 1000, null = True)
  Bill_To_Name = models.CharField(max_length = 1000, null = True)
  Bill_To_Address_1 = models.CharField(max_length = 1000, null = True)
  Bill_To_Address_2 = models.CharField(max_length = 1000, null = True)
  Bill_To_City = models.CharField(max_length = 1000, null = True)
  Bill_To_State = models.CharField(max_length = 1000, null = True)
  Bill_To_Zip = models.CharField(max_length = 1000, null = True)
  Bill_To_Country = models.CharField(max_length = 1000, null = True)
  Bill_To_Contact = models.CharField(max_length = 1000, null = True)
  Buying_Party_Name = models.CharField(max_length = 1000, null = True)
  Buying_Party_Location = models.CharField(max_length = 1000, null = True)
  Buying_Party_Address_1 = models.CharField(max_length = 1000, null = True)
  Buying_Party_Address_2 = models.CharField(max_length = 1000, null = True)
  Buying_Party_City = models.CharField(max_length = 1000, null = True)
  Buying_Party_State = models.CharField(max_length = 1000, null = True)
  Buying_Party_Zip = models.CharField(max_length = 1000, null = True)
  Buying_Party_Country = models.CharField(max_length = 1000, null = True)
  Buying_Party_Contact = models.CharField(max_length = 1000, null = True)
  Ultimate_Location = models.CharField(max_length = 1000, null = True)
  Notes_Comments = models.CharField(max_length = 1000, null = True)
  Ship_To_Additional_Name = models.CharField(max_length = 1000, null = True)
  Ship_To_Additional_Name_2 = models.CharField(max_length = 1000, null = True)
  Bill_To_Additional_Name = models.CharField(max_length = 1000, null = True)
  Bill_To_Additional_Name_2 = models.CharField(max_length = 1000, null = True)
  Buyer_Additional_Name = models.CharField(max_length = 1000, null = True)
  Buyer_Additional_Name_2 = models.CharField(max_length = 1000, null = True)
  GTIN = models.CharField(max_length = 1000, null = True)
  PO_Total_Amount = models.DecimalField(decimal_places = 3, null = True, max_digits = 10)
  PO_Total_Weight = models.DecimalField(decimal_places = 3, null = True, max_digits = 10)
  PO_Total_UOM = models.CharField(max_length = 1000, null = True)
  Shipping_account_number = models.CharField(max_length = 1000, null = True)
  Mark_for_Name = models.CharField(max_length = 1000, null = True)
  Mark_for_Address_1 = models.CharField(max_length = 1000, null = True)
  Mark_for_Address_2 = models.CharField(max_length = 1000, null = True)
  Mark_for_City = models.CharField(max_length = 1000, null = True)
  Mark_for_State = models.CharField(max_length = 1000, null = True)
  Mark_for_Postal = models.BigIntegerField(null = True)
  Mark_for_Country = models.CharField(max_length = 1000, null = True)
  Shipping_Container_Code = models.CharField(max_length = 1000, null = True)
  National_Drug_Code = models.CharField(max_length = 1000, null = True)
  Expiration_Date = models.CharField(max_length = 1000, null = True)
  Dist = models.CharField(max_length = 1000, null = True)
  Scheduled_Quantity = models.CharField(max_length = 1000, null = True)
  Scheduled_Qty_UOM = models.CharField(max_length = 1000, null = True)
  Required_By_Date = models.CharField(max_length = 1000, null = True)
  Must_Arrive_By = models.CharField(max_length = 1000, null = True)
  Entire_Shipment = models.CharField(max_length = 1000, null = True)
  Agreement_Number = models.CharField(max_length = 1000, null = True)
  Additional_Vendor_Part = models.CharField(max_length = 1000, null = True)
  Buyer_Part_Number = models.CharField(max_length = 1000, null = True)
  Carrier_Details_Special_Handling = models.CharField(max_length = 1000, null = True)
  Restrictions_Conditions = models.CharField(max_length = 1000, null = True)

class SalesImport_fields(models.Model):
  field_names = models.CharField(max_length = 50, null = True)
  
# class SalesImport(models.Model):
#   RecordType
#   CustomerName* = 
#   InvoiceNumber* = 
#   Reference/Comment/Note = 
#   Product* = 
#   Quantity* = 
#   Price/Amount* = 
#   Discount = 
#   Tax = 
#   Total* = 
#   Account = 
#   TaxRule* = 
#   DropShip = 
#   CurrencyConversionRate = 
#   DatePaid* = 
#   CustomerContact = 
#   CustomerPhone = 
#   CustomerEmail = 
#   SalesRepresentative* = 
#   ShipmentRequiredByDate = 
#   YourBaseCurrency* = 
#   CustomerCurrency* = 
#   Terms = 
#   PriceTier = 
#   StockLocation = 
#   MemoOnInvoice = 
#   InvoiceDate*/ExpireDate = 
#   InvoiceDueDate = 
#   TaxInclusive* = 
#   ShippingAddressLine1* = 
#   ShippingAddressLine2 = 
#   ShipToOther* = 
#   ShippingCity* = 
#   ShippingProvince* = 
#   ShippingPostcode* = 
#   ShippingCountry* = 
#   ShipToCompany* = 
#   BillingAddressLine1* = 
#   BillingAddressLine2 = 
#   BillingCity* = 
#   BillingProvince* = 
#   BillingPostcode* = 
#   BillingCountry* = 
#   CreditNoteNumber = 
#   CreditNoteDate = 
#   CustomField1 = 
#   CustomField2 = 
#   CustomField3 = 
#   CustomField4 = 
#   CustomField5 = 
#   CustomField6 = 
#   CustomField7 = 
#   CustomField8 = 
#   CustomField9 = 
#   CustomField10 = 
#   CarrierCode = 
#   CarrierServiceCode = 
#   ShipToContact = 
#   ShippingNotes = 

  
class OMS_Customers(models.Model):
  Name = models.CharField(max_length = 1000, null = True)
  Status = models.CharField(max_length = 1000, null = True)
  Currency = models.CharField(max_length = 1000, null = True)
  PaymentTerm = models.CharField(max_length = 1000, null = True)
  TaxRule = models.CharField(max_length = 1000, null = True)
  AccountReceivable = models.IntegerField(null = True)
  SaleAccount = models.IntegerField(null = True)
  PriceTier = models.CharField(max_length = 1000, null = True)
  Discount = models.IntegerField(null = True)
  CreditLimit = models.IntegerField(null = True)
  Carrier = models.CharField(max_length = 1000, null = True)
  SalesRepresentative = models.CharField(max_length = 1000, null = True)
  Location = models.CharField(max_length = 1000, null = True)
  TaxNumber = models.CharField(max_length = 1000, null = True)
  Tags = models.CharField(max_length = 1000, null = True)
  AttributeSet = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute1 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute2 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute3 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute4 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute5 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute6 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute7 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute8 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute9 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute10 = models.CharField(max_length = 1000, null = True)
  Comments = models.CharField(max_length = 1000, null = True)
  ContactName = models.CharField(max_length = 1000, null = True)
  JobTitle = models.CharField(max_length = 1000, null = True)
  Phone = models.CharField(max_length = 1000, null = True)
  MobilePhone = models.CharField(max_length = 1000, null = True)
  Fax = models.CharField(max_length = 1000, null = True)
  Email = models.CharField(max_length = 1000, null = True)
  Website = models.CharField(max_length = 1000, null = True)
  ContactComment = models.CharField(max_length = 1000, null = True)
  ContactDefault = models.BooleanField(null = True)
  ContactIncludeInEmail = models.BooleanField(null = True)
  MarketingConsent = models.CharField(max_length = 1000, null = True)
  IsAccountingDimensionEnabled = models.BooleanField(null = True)
  DimensionAttribute1 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute2 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute3 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute4 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute5 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute6 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute7 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute8 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute9 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute10 = models.CharField(max_length = 1000, null = True)

class Ocustomer_fields(models.Model):
  field_name = models.CharField(max_length = 50)

class OMS_Inventory_List(models.Model):
  ProductCode = models.CharField(max_length = 1000, null = True)
  Name = models.CharField(max_length = 1000, null = True)
  Category = models.CharField(max_length = 1000, null = True)
  Brand = models.CharField(max_length = 1000, null = True)
  Type = models.CharField(max_length = 1000, null = True)
  FixedAssetType = models.CharField(max_length = 1000, null = True)
  CostingMethod = models.CharField(max_length = 1000, null = True)
  Length = models.CharField(max_length = 1000, null = True)
  Width = models.CharField(max_length = 1000, null = True)
  Height = models.CharField(max_length = 1000, null = True)
  Weight = models.CharField(max_length = 1000, null = True)
  CartonLength = models.CharField(max_length = 1000, null = True)
  CartonWidth = models.CharField(max_length = 1000, null = True)
  CartonHeight = models.CharField(max_length = 1000, null = True)
  CartonInnerQuantity = models.CharField(max_length = 1000, null = True)
  CartonQuantity = models.CharField(max_length = 1000, null = True)
  CartonVolume = models.CharField(max_length = 1000, null = True)
  WeightUnits = models.CharField(max_length = 1000, null = True)
  DimensionUnits = models.CharField(max_length = 1000, null = True)
  Barcode = models.CharField(max_length = 1000, null = True)
  MinimumBeforeReorder = models.IntegerField(null = True)
  ReorderQuantity = models.IntegerField(null = True)
  DefaultLocation = models.CharField(max_length = 1000, null = True)
  LastSuppliedBy = models.CharField(max_length = 1000, null = True)
  SupplierProductCode = models.CharField(max_length = 1000, null = True)
  SupplierProductName = models.CharField(max_length = 1000, null = True)
  SupplierFixedPrice = models.CharField(max_length = 1000, null = True)
  PriceTier1 = models.CharField(max_length = 1000, null = True)
  PriceTier2 = models.CharField(max_length = 1000, null = True)
  PriceTier3 = models.CharField(max_length = 1000, null = True)
  PriceTier4 = models.CharField(max_length = 1000, null = True)
  PriceTier5 = models.CharField(max_length = 1000, null = True)
  PriceTier6 = models.CharField(max_length = 1000, null = True)
  PriceTier7 = models.CharField(max_length = 1000, null = True)
  PriceTier8 = models.CharField(max_length = 1000, null = True)
  PriceTier9 = models.CharField(max_length = 1000, null = True)
  PriceTier10 = models.CharField(max_length = 1000, null = True)
  AssemblyBOM = models.CharField(max_length = 1000, null = True)
  AutoAssemble = models.CharField(max_length = 1000, null = True)
  AutoDisassemble = models.CharField(max_length = 1000, null = True)
  DropShip = models.CharField(max_length = 1000, null = True)
  DropShipSupplier = models.CharField(max_length = 1000, null = True)
  AverageCost = models.CharField(max_length = 1000, null = True)
  DefaultUnitOfMeasure = models.CharField(max_length = 1000, null = True)
  InventoryAccount = models.CharField(max_length = 1000, null = True)
  RevenueAccount = models.CharField(max_length = 1000, null = True)
  ExpenseAccount = models.CharField(max_length = 1000, null = True)
  COGSAccount = models.CharField(max_length = 1000, null = True)
  ProductAttributeSet = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute1 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute2 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute3 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute4 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute5 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute6 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute7 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute8 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute9 = models.CharField(max_length = 1000, null = True)
  AdditionalAttribute10 = models.CharField(max_length = 1000, null = True)
  DiscountName = models.CharField(max_length = 1000, null = True)
  ProductFamilySKU = models.CharField(max_length = 1000, null = True)
  ProductFamilyName = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption1Name = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption1Value = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption2Name = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption2Value = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption3Name = models.CharField(max_length = 1000, null = True)
  ProductFamilyOption3Value = models.CharField(max_length = 1000, null = True)
  CommaDelimitedTags = models.CharField(max_length = 1000, null = True)
  StockLocator = models.CharField(max_length = 1000, null = True)
  PurchaseTaxRule = models.CharField(max_length = 1000, null = True)
  SaleTaxRule = models.CharField(max_length = 1000, null = True)
  Status = models.CharField(max_length = 1000, null = True)
  Description = models.CharField(max_length = 1000, null = True)
  ShortDescription = models.CharField(max_length = 1000, null = True)
  Sellable = models.CharField(max_length = 1000, null = True)
  PickZones = models.CharField(max_length = 1000, null = True)
  AlwaysShowQuantity = models.CharField(max_length = 1000, null = True)
  WarrantySetupName = models.CharField(max_length = 1000, null = True)
  InternalNote = models.CharField(max_length = 1000, null = True)
  ProductionBOM = models.CharField(max_length = 1000, null = True)
  MakeToOrderBom = models.CharField(max_length = 1000, null = True)
  QuantityToProduce = models.IntegerField(null = True)
  IsAccountingDimensionEnabled = models.BooleanField(null = True)
  DimensionAttribute1 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute2 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute3 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute4 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute5 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute6 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute7 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute8 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute9 = models.CharField(max_length = 1000, null = True)
  DimensionAttribute10 = models.CharField(max_length = 1000, null = True)
  HSCode = models.CharField(max_length = 1000, null = True)
  CountryOfOrigin = models.CharField(max_length = 1000, null = True)

class Oinventory_fields(models.Model):
  field_name = models.CharField(max_length = 50)

class OMS_Payment_term(models.Model):
  Name = models.CharField(max_length = 1000, null = True)
  Days = models.IntegerField(null = True)
  Method = models.IntegerField(null = True)
  DueNextMonth = models.IntegerField(null = True)
  PaymentTermActive = models.BooleanField(null = True)
  PaymentTermDefault = models.BooleanField(null = True)

class OMS_AdditionalUOM(models.Model):
  Action = models.CharField(max_length = 1000, null = True)
  BaseSKU = models.CharField(max_length = 1000, null = True)
  BaseProductName = models.CharField(max_length = 1000, null = True)
  BaseUnitsOfMeasure = models.CharField(max_length = 1000, null = True)
  AdditionalUnitsOfMeasureSKU = models.CharField(max_length = 1000, null = True)
  AdditionalUnitsOfMeasureProductName = models.CharField(max_length = 1000, null = True)
  AdditionalUnitsOfMeasureName = models.CharField(max_length = 1000, null = True)
  NumberOfBaseUnitsInAdditionalUnit = models.IntegerField(null = True)
  IAmSellingThisProduct = models.BooleanField(null = True)

class OMS_UOM(models.Model):
  Name = models.CharField(max_length = 1000, null = True)

class OMS_Locations(models.Model):
  Location = models.CharField(max_length = 1000, null = True)

class Olocation_fields(models.Model):
  field_name = models.CharField(max_length = 50)

class Input_paths(models.Model):
  path = models.CharField(max_length = 200, null = True)
  file_name = models.CharField(max_length = 200, null = True)
  created = models.CharField(max_length = 1000, null = True)