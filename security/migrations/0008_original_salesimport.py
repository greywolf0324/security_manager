# Generated by Django 4.2.7 on 2024-01-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0007_customers_sku_bl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Original_SalesImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PO_Number', models.BigIntegerField()),
                ('Release_Number', models.BigIntegerField(null=True)),
                ('PO_Date', models.DateField(null=True)),
                ('Dept', models.CharField(max_length=255, null=True)),
                ('Retailers_PO', models.BigIntegerField()),
                ('Requested_Delivery_Date', models.DateField(null=True)),
                ('Delivery_Dates', models.DateField(null=True)),
                ('Ship_Dates', models.DateField(null=True)),
                ('Cancel_Date', models.DateField(null=True)),
                ('Carrier', models.CharField(max_length=255, null=True)),
                ('Carrier_Details', models.CharField(max_length=255, null=True)),
                ('Ship_To_Location', models.IntegerField(null=True)),
                ('PO_Line', models.IntegerField(null=True)),
                ('Qty_Ordered', models.IntegerField(null=True)),
                ('Unit_of_Measure', models.CharField(max_length=20, null=True)),
                ('Unit_Price', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('Buyers_Catalog_or_Stock_Keeping', models.BigIntegerField(null=True)),
                ('UPC_EAN', models.BigIntegerField(null=True)),
                ('Vendor_Style', models.IntegerField(null=True)),
                ('Retail_Price', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('Product_Item_Description', models.CharField(max_length=1000, null=True)),
                ('Color', models.CharField(max_length=255, null=True)),
                ('Size', models.CharField(max_length=20, null=True)),
                ('Pack_Size', models.CharField(max_length=255, null=True)),
                ('Pack_Size_UOM', models.CharField(max_length=10, null=True)),
                ('Number_of_Inner_Packs', models.IntegerField(null=True)),
                ('Number_of_Pcs_per_Inner_Pack', models.IntegerField(null=True)),
                ('Store', models.CharField(max_length=10, null=True)),
                ('Qty_per_Store', models.IntegerField(null=True)),
                ('Record_Type', models.CharField(max_length=10, null=True)),
                ('PO_purpose', models.CharField(max_length=255, null=True)),
                ('PO_Type', models.CharField(max_length=255, null=True)),
                ('Contract_Number', models.CharField(max_length=255, null=True)),
                ('Currency', models.CharField(max_length=255, null=True)),
                ('Ship_Status', models.CharField(max_length=255, null=True)),
                ('Letter_of_Credit', models.CharField(max_length=255, null=True)),
                ('Vendor', models.IntegerField(null=True)),
                ('Division', models.CharField(max_length=255, null=True)),
                ('Cust_Acct', models.CharField(max_length=255, null=True)),
                ('Customer_Order', models.CharField(max_length=255, null=True)),
                ('Promo', models.CharField(max_length=255, null=True)),
                ('Ticket_Description', models.CharField(max_length=255, null=True)),
                ('Other_Info', models.CharField(max_length=255, null=True)),
                ('Frt_Terms', models.CharField(max_length=255, null=True)),
                ('Carrier_Service_Level', models.CharField(max_length=255, null=True)),
                ('Payment_Terms', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Disc_Due_Date', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Disc_Days_Due', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Net_Due_Date', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Net_Days', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Disc_Amt', models.CharField(max_length=255, null=True)),
                ('Payment_Terms_Desc', models.CharField(max_length=255, null=True)),
                ('Contact_Phone', models.CharField(max_length=255, null=True)),
                ('Contact_Fax', models.CharField(max_length=255, null=True)),
                ('Contact_Email', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Type', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Service', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Amt', models.CharField(max_length=255, null=True)),
                ('AllowCharge', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Rate', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Qty', models.CharField(max_length=255, null=True)),
                ('AllowCharge_Desc', models.CharField(max_length=255, null=True)),
                ('Ship_To_Name', models.CharField(max_length=255, null=True)),
                ('Ship_To_Address_1', models.CharField(max_length=255, null=True)),
                ('Ship_To_Address_2', models.CharField(max_length=255, null=True)),
                ('Ship_To_City', models.CharField(max_length=255, null=True)),
                ('Ship_To_State', models.CharField(max_length=255, null=True)),
                ('Ship_to_Zip', models.IntegerField(null=True)),
                ('Ship_To_Country', models.CharField(max_length=255, null=True)),
                ('Ship_To_Contact', models.CharField(max_length=255, null=True)),
                ('Bill_To_Name', models.CharField(max_length=255, null=True)),
                ('Bill_To_Address_1', models.CharField(max_length=255, null=True)),
                ('Bill_To_Address_2', models.CharField(max_length=255, null=True)),
                ('Bill_To_City', models.CharField(max_length=255, null=True)),
                ('Bill_To_State', models.CharField(max_length=255, null=True)),
                ('Bill_To_Zip', models.IntegerField(null=True)),
                ('Bill_To_Country', models.CharField(max_length=255, null=True)),
                ('Bill_To_Contact', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Name', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Location', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Address_1', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Address_2', models.CharField(max_length=255, null=True)),
                ('Buying_Party_City', models.CharField(max_length=255, null=True)),
                ('Buying_Party_State', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Zip', models.IntegerField(null=True)),
                ('Buying_Party_Country', models.CharField(max_length=255, null=True)),
                ('Buying_Party_Contact', models.CharField(max_length=255, null=True)),
                ('Ultimate_Location', models.CharField(max_length=255, null=True)),
                ('Notes_Comments', models.CharField(max_length=255, null=True)),
                ('Ship_To_Additional_Name', models.CharField(max_length=255, null=True)),
                ('Ship_To_Additional_Name_2', models.CharField(max_length=255, null=True)),
                ('Bill_To_Additional_Name', models.CharField(max_length=255, null=True)),
                ('Bill_To_Additional_Name_2', models.CharField(max_length=255, null=True)),
                ('Buyer_Additional_Name', models.CharField(max_length=255, null=True)),
                ('Buyer_Additional_Name_2', models.CharField(max_length=255, null=True)),
                ('GTIN', models.CharField(max_length=255, null=True)),
                ('PO_Total_Amount', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('PO_Total_Weight', models.DecimalField(decimal_places=3, max_digits=10, null=True)),
                ('PO_Total_UOM', models.CharField(max_length=255, null=True)),
                ('Shipping_account_number', models.CharField(max_length=255, null=True)),
                ('Mark_for_Name', models.CharField(max_length=255, null=True)),
                ('Mark_for_Address_1', models.CharField(max_length=255, null=True)),
                ('Mark_for_Address_2', models.CharField(max_length=255, null=True)),
                ('Mark_for_City', models.CharField(max_length=255, null=True)),
                ('Mark_for_State', models.CharField(max_length=255, null=True)),
                ('Mark_for_Postal', models.IntegerField(null=True)),
                ('Mark_for_Country', models.CharField(max_length=255, null=True)),
                ('Shipping_Container_Code', models.CharField(max_length=255, null=True)),
                ('National_Drug_Code', models.CharField(max_length=255, null=True)),
                ('Expiration_Date', models.CharField(max_length=255, null=True)),
                ('Dist', models.CharField(max_length=255, null=True)),
                ('Scheduled_Quantity', models.CharField(max_length=255, null=True)),
                ('Scheduled_Qty_UOM', models.CharField(max_length=255, null=True)),
                ('Required_By_Date', models.CharField(max_length=255, null=True)),
                ('Must_Arrive_By', models.CharField(max_length=255, null=True)),
                ('Entire_Shipment', models.CharField(max_length=255, null=True)),
                ('Agreement_Number', models.CharField(max_length=255, null=True)),
                ('Additional_Vendor_Part', models.CharField(max_length=255, null=True)),
                ('Buyer_Part_Number', models.CharField(max_length=255, null=True)),
                ('Carrier_Details_Special_Handling', models.CharField(max_length=255, null=True)),
                ('Restrictions_Conditions', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
