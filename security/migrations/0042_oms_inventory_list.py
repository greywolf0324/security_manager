# Generated by Django 4.2.7 on 2024-01-05 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0041_delete_oms_inventory_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='OMS_Inventory_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductCode', models.CharField(max_length=1000, null=True)),
                ('Name', models.CharField(max_length=1000, null=True)),
                ('Category', models.CharField(max_length=1000, null=True)),
                ('Brand', models.CharField(max_length=1000, null=True)),
                ('Type', models.CharField(max_length=1000, null=True)),
                ('FixedAssetType', models.CharField(max_length=1000, null=True)),
                ('CostingMethod', models.CharField(max_length=1000, null=True)),
                ('Length', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Width', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Height', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('Weight', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonLength', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonWidth', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonHeight', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonInnerQuantity', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonQuantity', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('CartonVolume', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('WeightUnits', models.CharField(max_length=1000, null=True)),
                ('DimensionUnits', models.CharField(max_length=1000, null=True)),
                ('Barcode', models.BigIntegerField(null=True)),
                ('MinimumBeforeReorder', models.IntegerField(null=True)),
                ('ReorderQuantity', models.IntegerField(null=True)),
                ('DefaultLocation', models.CharField(max_length=1000, null=True)),
                ('LastSuppliedBy', models.CharField(max_length=1000, null=True)),
                ('SupplierProductCode', models.CharField(max_length=1000, null=True)),
                ('SupplierProductName', models.CharField(max_length=1000, null=True)),
                ('SupplierFixedPrice', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier1', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier2', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier3', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier4', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier5', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier6', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier7', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier8', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier9', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('PriceTier10', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('AssemblyBOM', models.CharField(max_length=1000, null=True)),
                ('AutoAssemble', models.CharField(max_length=1000, null=True)),
                ('AutoDisassemble', models.CharField(max_length=1000, null=True)),
                ('DropShip', models.CharField(max_length=1000, null=True)),
                ('DropShipSupplier', models.CharField(max_length=1000, null=True)),
                ('AverageCost', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('DefaultUnitOfMeasure', models.CharField(max_length=1000, null=True)),
                ('InventoryAccount', models.CharField(max_length=1000, null=True)),
                ('RevenueAccount', models.CharField(max_length=1000, null=True)),
                ('ExpenseAccount', models.CharField(max_length=1000, null=True)),
                ('COGSAccount', models.CharField(max_length=1000, null=True)),
                ('ProductAttributeSet', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute1', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute2', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute3', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute4', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute5', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute6', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute7', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute8', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute9', models.CharField(max_length=1000, null=True)),
                ('AdditionalAttribute10', models.CharField(max_length=1000, null=True)),
                ('DiscountName', models.CharField(max_length=1000, null=True)),
                ('ProductFamilySKU', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyName', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption1Name', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption1Value', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption2Name', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption2Value', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption3Name', models.CharField(max_length=1000, null=True)),
                ('ProductFamilyOption3Value', models.CharField(max_length=1000, null=True)),
                ('CommaDelimitedTags', models.CharField(max_length=1000, null=True)),
                ('StockLocator', models.CharField(max_length=1000, null=True)),
                ('PurchaseTaxRule', models.CharField(max_length=1000, null=True)),
                ('SaleTaxRule', models.CharField(max_length=1000, null=True)),
                ('Status', models.CharField(max_length=1000, null=True)),
                ('Description', models.CharField(max_length=1000, null=True)),
                ('ShortDescription', models.CharField(max_length=1000, null=True)),
                ('Sellable', models.CharField(max_length=1000, null=True)),
                ('PickZones', models.CharField(max_length=1000, null=True)),
                ('AlwaysShowQuantity', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('WarrantySetupName', models.CharField(max_length=1000, null=True)),
                ('InternalNote', models.CharField(max_length=1000, null=True)),
                ('ProductionBOM', models.CharField(max_length=1000, null=True)),
                ('MakeToOrderBom', models.CharField(max_length=1000, null=True)),
                ('QuantityToProduce', models.IntegerField(null=True)),
                ('IsAccountingDimensionEnabled', models.BooleanField(null=True)),
                ('DimensionAttribute1', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute2', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute3', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute4', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute5', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute6', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute7', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute8', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute9', models.CharField(max_length=1000, null=True)),
                ('DimensionAttribute10', models.CharField(max_length=1000, null=True)),
                ('HSCode', models.CharField(max_length=1000, null=True)),
                ('CountryOfOrigin', models.CharField(max_length=1000, null=True)),
            ],
        ),
    ]
