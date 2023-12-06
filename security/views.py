from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import ProcessForm
from .OMS_Data_engineering.functions import SalesImport_Generator
from .OMS_Data_engineering.utils.analyzer import Input_analyzer, Output_analyzer
from .models import ProcessHistory
from django.http import HttpResponse, JsonResponse
import mimetypes
import json
import os
from glob import glob
from pathlib import Path

# These are first productions for our site and for this customer.
# Do you want to use them to auto-fill for further times?
generator = SalesImport_Generator()
customer_list = [
    "Buc-ee's",
    "Pepco",
    "Poundland",
    "Walgreens",
    "Dollarama",
    "Family Dollar",
    "Gabe's",
    "TEDI",
    "Walmart",
    "Ollies",
    "Big Lots Stores",
    "TARGET",
    "CVS",
    "Five Below",
    "Meijers",
    "MICHAELS",
    "Fred Meyer",
    "Tar Heel Trading",
    # "Giant Tiger",
    # "Hobby Lobby",
    # "Lekia",
]

customer_list.sort()

# Create your views here.
@login_required
def home(request):
  user = request.user
  if request.method == 'POST':
    files = request.FILES.getlist('data')
    matching_res = json.loads(request.POST['input'])
    customername = request.POST['customername']
    termOptions = json.loads(request.POST['termOptions'])
    # if customername == "Buc-ee's":
      # res = generator.processFile(files, matching_res, {}, customername, termOptions)
    # if customername == "Pepco":
      # currency = request.POST['currency']
    
    res = generator.processFile(files, matching_res, {}, customername, termOptions)
    # res_view = generator.res_viewer(matching_res, customername, termOptions)
    if res == "fail":
      return JsonResponse({ "message": "You need to update database" }, status=400)
    history = ProcessHistory.objects.create(user=user, input=res[0], output=res[1], )

    return JsonResponse({ "id": history.id }, status=200)


  options = ["99 Cents Only Stores", "AIS LTD - USD", "ALBERT HARRISON", "ALLYSON PETTY", "ALLYSON PETTY", "Amazon Import - BEAZB", "Amazon Seller Central", "Anderson's Bookshop ", "Apple Annie's", "Argyle Toys", "BARGAINMAX", "BARNES & NOBLE", "Bealls", "BigLots ", "BMI", "BMS", "Bow Love", "BRANDI BRAVO", "BUC-EE'S", "CARL MILLER", "Cascade", "CASSIE GLUCK", "CASSIE GLUCK", "CHRISTINE TAYLOR", "Christophe Mennes", "CINDY HEDDAEUS", "CK", "CKEU LTD", "CM School Supply", "Conscious Discipline", "Coppel", "CORPORACION EL ROSADO S.A.", "Creative Kids Far East Inc.", "Creative Kids Online", "CRYSTAL WALKER", "CVS", "CYNTHIA FUSSY", "CYP BRANDS", "DARIUS MOSLEY", "Default Shopify Customer", "DISCOVERY CHILDREN'S MUSEUM", "DKB GBP", "DKB USD", "Dollar General", "Dollar General Domestic", "Dollar Tree", "DONITA LYNNE SMITH", "DONNA GINEVAN", "Dylan\u2019s Candy Bar", "EDUCATIONAL SERVICES", "EDUCATIONAL SERVICES", "Educators Resource", "EDUCTAORS RESOURCE", "ELEGANT MOMMY", "Elephants Trunk", "ENCORE", "ERIN DICKSON", "FABIOLA DE LEON", "Family Dollar", "FEB", "Five Below", "GEPPETTO", "Giant Tiger", "Goodthings Inc", "Grandrabbits Toy Shoppe", "Grocery Outlet", "HANA ZUCKER", "HARRODS", "HOBBYCRAFT", "Hudson", "Jennifer Welsch", "JESSICA GREEN", "Joann", "JOANNA OWEN", "JOANNA OWEN", "JOSEPH SIMPSON", "KEAGAN WICKERHAM", "KEELA LINDSAY", "KELLY PETERSON", "KOHLS", "KURTZ BROS. ", "LAURA MERRITT", "LEARNING EXPRESS", "Learning Gizmos", "Lekia", "LHU MILES", "LISA KANE CHARLES", "LOUISA ODLYZKO", "Love's Pharmacy & Gifts- Pass Christian", "MARK RYSAVY", "MARLENE WALKER", "MARSHALLS", "MCPS S EDUCATION", "MCPS S EDUCATION", "MICHAELS", "Mix Sales & Services", "Nasa Toys Panama", "NASCO", "National Energy Foundation", "NORTH EASTERN", "ORBICO", "Over The Rainbow Toys", "Pacifier", "PATRICIA BUCK", "PEEK A BOO", "Pepco", "Pepco - EUR", "Pepco - RMB", "Pepco - USD", "Pop Shelf", "Poundland - RMB", "PREMIUM", "Rainbow Resource Center", "REBECCA CLYMER", "Red Planet Group", "Rite Aid", "ROBIN MORAN", "S&S Worldwide", "SARAH ROLLINGS", "SARAH WRIGHT", "SAVANNAH KOON", "Scottwood Floral", "SHACOBY BAILEY", "Shady Maple", "SHANNA GRIFFIN", "SMF", "SMG", "Snapdoodle Toys & Games", "SUE STRUTZ", "TARGET", "TELEVIEW", "TFH USA", "The Paper Store", "THE WORKS", "THE WORKS - USD", "Therapro", "THERESA JUHAS", "THERESA JUHAS", "Timberdoodle", "TJMAXX", "TONY RUBOLINO", "TOYLAND", "Toyology", "Urbana Arcadia Toys", "VENESSA ORLUCK SACC PROGRAM", "VENESSA ORLUCK SACC PROGRAM", "VIRGINIA CATA", "VWR", "Walgreens", "Walmart Canada", "Walmart US", "WH Smith", "WHSmith High Street Limited", "Wonder Works", "WT & T", "YOLUNDA GILES"]

  return render(request, 'home.html', { "options": options })

@login_required
def viewer(request):
  if request.method == 'POST':
    files = request.FILES.getlist('data')
    matching_res = json.loads(request.POST['input'])
    customername = request.POST['customername']
    termOptions = json.loads(request.POST['termOptions'])
    # if customername == "Buc-ee's":
      # res = generator.processFile(files, matching_res, {}, customername, termOptions)
    # if customername == "Pepco":
      # currency = request.POST['currency']
    res = generator.res_viewer(files, matching_res, customername, termOptions)
    if res == "fail":
      return JsonResponse({ "message": "You need to update database" }, status=400)
    return JsonResponse({ "res": json.dumps(res) }, status=200)


  options = ["99 Cents Only Stores", "AIS LTD - USD", "ALBERT HARRISON", "ALLYSON PETTY", "ALLYSON PETTY", "Amazon Import - BEAZB", "Amazon Seller Central", "Anderson's Bookshop ", "Apple Annie's", "Argyle Toys", "BARGAINMAX", "BARNES & NOBLE", "Bealls", "BigLots ", "BMI", "BMS", "Bow Love", "BRANDI BRAVO", "BUC-EE'S", "CARL MILLER", "Cascade", "CASSIE GLUCK", "CASSIE GLUCK", "CHRISTINE TAYLOR", "Christophe Mennes", "CINDY HEDDAEUS", "CK", "CKEU LTD", "CM School Supply", "Conscious Discipline", "Coppel", "CORPORACION EL ROSADO S.A.", "Creative Kids Far East Inc.", "Creative Kids Online", "CRYSTAL WALKER", "CVS", "CYNTHIA FUSSY", "CYP BRANDS", "DARIUS MOSLEY", "Default Shopify Customer", "DISCOVERY CHILDREN'S MUSEUM", "DKB GBP", "DKB USD", "Dollar General", "Dollar General Domestic", "Dollar Tree", "DONITA LYNNE SMITH", "DONNA GINEVAN", "Dylan\u2019s Candy Bar", "EDUCATIONAL SERVICES", "EDUCATIONAL SERVICES", "Educators Resource", "EDUCTAORS RESOURCE", "ELEGANT MOMMY", "Elephants Trunk", "ENCORE", "ERIN DICKSON", "FABIOLA DE LEON", "Family Dollar", "FEB", "Five Below", "GEPPETTO", "Giant Tiger", "Goodthings Inc", "Grandrabbits Toy Shoppe", "Grocery Outlet", "HANA ZUCKER", "HARRODS", "HOBBYCRAFT", "Hudson", "Jennifer Welsch", "JESSICA GREEN", "Joann", "JOANNA OWEN", "JOANNA OWEN", "JOSEPH SIMPSON", "KEAGAN WICKERHAM", "KEELA LINDSAY", "KELLY PETERSON", "KOHLS", "KURTZ BROS. ", "LAURA MERRITT", "LEARNING EXPRESS", "Learning Gizmos", "Lekia", "LHU MILES", "LISA KANE CHARLES", "LOUISA ODLYZKO", "Love's Pharmacy & Gifts- Pass Christian", "MARK RYSAVY", "MARLENE WALKER", "MARSHALLS", "MCPS S EDUCATION", "MCPS S EDUCATION", "MICHAELS", "Mix Sales & Services", "Nasa Toys Panama", "NASCO", "National Energy Foundation", "NORTH EASTERN", "ORBICO", "Over The Rainbow Toys", "Pacifier", "PATRICIA BUCK", "PEEK A BOO", "Pepco", "Pepco - EUR", "Pepco - RMB", "Pepco - USD", "Pop Shelf", "Poundland - RMB", "PREMIUM", "Rainbow Resource Center", "REBECCA CLYMER", "Red Planet Group", "Rite Aid", "ROBIN MORAN", "S&S Worldwide", "SARAH ROLLINGS", "SARAH WRIGHT", "SAVANNAH KOON", "Scottwood Floral", "SHACOBY BAILEY", "Shady Maple", "SHANNA GRIFFIN", "SMF", "SMG", "Snapdoodle Toys & Games", "SUE STRUTZ", "TARGET", "TELEVIEW", "TFH USA", "The Paper Store", "THE WORKS", "THE WORKS - USD", "Therapro", "THERESA JUHAS", "THERESA JUHAS", "Timberdoodle", "TJMAXX", "TONY RUBOLINO", "TOYLAND", "Toyology", "Urbana Arcadia Toys", "VENESSA ORLUCK SACC PROGRAM", "VENESSA ORLUCK SACC PROGRAM", "VIRGINIA CATA", "VWR", "Walgreens", "Walmart Canada", "Walmart US", "WH Smith", "WHSmith High Street Limited", "Wonder Works", "WT & T", "YOLUNDA GILES"]

  return render(request, 'home.html', { "options": options })

def auto_matching_DB_viewer(request):
  res=generator.auto_matching_DB_viewer(customer_name)
  customer_name=request.POST['customer_name']
  return JsonResponse({"data":json.dumps(res)}, status=200)

@login_required
def parseUpload(request):
  files = request.FILES.getlist('data')
  customer_name = request.POST['customername']
  # if customer_name == "Buc-ee's":
  #   # currency = ""
  #   res = generator.parseUpload(files, customer_name = customer_name)

  if customer_name == "Pepco":
    currency = request.POST['currency']
    res = generator.parseUpload(files, customer_name = customer_name, currency = currency)
    
  else:
    res = generator.parseUpload(files, customer_name = customer_name)

  return JsonResponse({ "data1": json.dumps(res[0]), "data2": json.dumps(res[1]), "data3": json.dumps(res[2]), "data4": json.dumps(res[3]), "data5": json.dumps(res[4]) }, status=200)

@login_required
def requiredItems(request):
  if request.method == 'POST':
    input = json.loads(request.POST["input"])
    res = generator.requiredFields(input)
    return JsonResponse({ "fields": res }, status=200)
  
@login_required
def history(request):
  user = request.user
  histories = ProcessHistory.objects.filter(user=user).order_by('-id')

  print(histories[0].user)
  print(histories[0].input)
  print(histories[0].output)
  print(histories[0].created_at)
  print(histories[0].updated_at)
  # History Generation
  path = Path(__file__).resolve().parent.parent / "process/outputs"
  os.chdir(path)
  paths = []
  
  view_dir = Path(__file__).resolve().parent.parent / "process/views"
  view_paths = os.listdir(view_dir)
  view_filename_paths = []
  for view_path in view_paths:
    view_filename_paths.append(view_path[:-4])
    
  for file in glob("*.csv"):
    print(path)
    print(file)
    if file[:-3] in view_filename_paths:
      paths.append(str(path) + "\\" + file)

  print("+++++++++++++++++++++++++++++++++++")
  print(paths)
  print("+++++++++++++++++++++++++++++++++++")
  new_histories = []
  creation_dates = []
  print("_____________________________")
  # print(type(paths[0]))
  history_location = []
  for history in histories:
    history_location.append(str(history.output))
  
  for history in histories:
    if str(history.output) in paths:
      creation_dates.append(str(history.created_at))
      new_histories.append(history)
  
  print("**********************")
  print(new_histories)
  print("**********************")

  file_contents = []
  for history in new_histories:
    # f = open((Path(__file__).resolve().parent.parent.parent / history.output), 'rb')
    with open(Path(__file__).resolve().parent.parent / history.output, 'rb') as f:
      file_contents.append(f.read())
  # print(file_contents)
  if len(file_contents) == 0:
    histories = "empty"

  else:
    [customer_names, PO_dates] = Output_analyzer(file_contents)

    users = []
    for history in new_histories:
      users.append(str(history.user).split("@")[0])
    # print(customer_names, users, creation_dates, PO_dates, type(PO_dates[0]))
    # histories = zip(customer_names, users, creation_dates, PO_dates)
    
    histories = zip(customer_names, users, creation_dates, PO_dates)
  
  return render(request, 'history.html', {"histories": histories, "real": paths, "history": history_location, "new": new_histories})
  
  # else:
  #   return render(request, 'history.html', {"histories": "empty"})
    # return render(request, 'history.html', {"histories": zip([""], [""], [""], [""])})
  # return JsonResponse({ "customer_names": json.dumps(customer_names), "users": json.dumps(users), "creation_dates": json.dumps(creation_dates), "PO_dates": json.dumps(PO_dates) }, status = 200)

@login_required
def history_viewer(request, creation_date):
  histories = ProcessHistory.objects.all()
  for history in histories:
    if str(history.created_at) == creation_date:
      db_name = str(history.output)
      break
  # print(db_name[:-59], "!!!!!!!!!!!!!!!!!!!!!!!!")
  # print(db_name[-51:-3], "!!!!!!!!!!!!!!!!!!!!!!!!")
  # history = ProcessHistory.objects.get(creation_date = creation_date)
  # with open((Path(__file__).resolve().parent.parent / history.output), 'rb') as f:
  #   customer_name = Output_analyzer([f.read()])[0][0]
  # with open((Path(__file__).resolve().parent.parent / history.input), 'r') as f:
  file_name = db_name[:-59] + "views/" + db_name[-51:-3] + "json"
  # print(file_name)
  with open(file_name) as f:
    db = json.load(f)
  
  customername = db[0]
  headerkeys = []
  itemkeys = []
  headerdetails = []
  itemdetails = []

  for key in db[1][0].keys():
    headerkeys.append(key)
  
  for key in db[2][0].keys():
    itemkeys.append(key)

  for line in db[1]:
    temp = []
    for key, values in line.items():
      temp.append(values[0])
    
    headerdetails.append(temp)

  for line in db[2]:
    temp = []
    for key, values in line.items():
      temp.append(values)

    dic = []
    for j in range(len(temp[0])):
      tem_dic = []
      for i in range(len(temp)):
        tem_dic.append(temp[i][j])
      
      dic.append(tem_dic)
    
    itemdetails.append(dic)

  print(headerdetails[0])
  print(itemdetails[0])
  print(itemdetails)
  # return JsonResponse(responser, status=200)
  return render(request, 'history_view.html', {'customername': customername, "headerkeys": headerkeys, "itemkeys": itemkeys, "details": zip(headerdetails, itemdetails)})

@login_required
def history_deletion(request):
    histories = ProcessHistory.objects.all()
    print(len(histories), "=================================")
    path_outputs = Path(__file__).resolve().parent.parent / "process/outputs"
    # for history in histories:
    #   # if str(history.created_at) in creation_dates:
    #   print(history.)
        
    os.chdir(path_outputs)
    # for file in glob("*.csv"):
    path_inputs = Path(__file__).resolve().parent.parent / "process/inputs"
    path_views = Path(__file__).resolve().parent.parent / "process/views"
    try:
        data = json.loads(request.body.decode('utf-8'))
        creation_dates = data.get('creationDates')
        print(creation_dates)
        if creation_dates:
            for history in histories:
              if str(history.created_at) in creation_dates:
                print("===================")
                print(history.output, "============")
                print(history.input, "============")
                temp = str(history.output)
                temp = temp.replace("outputs", "views")
                temp = temp.replace("csv", "json")
                print(temp, "===========")
                history.delete()
                os.remove(str(history.output))
                os.remove(str(history.input))
                os.remove(temp)
              # ProcessHistory.objects.filter(str(history.created_at) in creation_dates).delete()
              # print("deleted!!!!!!!!!!")
            
            print(creation_dates, "Deletion successful")
            return JsonResponse({'message': 'Deletion successful'})
        else:
            print("No creation dates received")
            return JsonResponse({'message': 'No creation dates received'}, status=400)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", str(e))
        return JsonResponse({'message': 'Error decoding JSON'}, status=400)

def POconversion(request):
  customername = request.GET.get('customer-name', customer_list[0])
  conversion = generator.auto_matching_DB_viewer(customername)
  if type(conversion) != str:
    
    combined_values = zip(conversion["PO"], conversion["UOM"], conversion["LOCATION"], conversion["TARGET"])
    
    uom_options = conversion["UOM_options"]
    location_options = conversion["location_options"]
    vendor_options = conversion["vendor_options"]
    
    # print(conversion["LOCATION"])
    # return JsonResponse({ "customername": customername, "conversion": combined_values, "customers": customer_list })
    return render(request, 'POconversion.html', { "customername": customername, "conversion":combined_values,"customers": customer_list, "uom_options": uom_options, "location_options": location_options, "vendor_options": vendor_options })

  else:

    # return JsonResponse({ "customername": customername, "conversion": "non-exists", "customers": customer_list })
    return  render(request, 'POconversion.html', { "customername": customername, "conversion":"non-exists","customers": customer_list })

@login_required
def downloadFile(request, id):
  history = ProcessHistory.objects.get(id=id)
  file_path = history.output
  
  with open(file_path, 'rb') as f:
    file_content = f.read()
  content_type, _ = mimetypes.guess_type(file_path)
  response = HttpResponse(file_content, content_type=content_type)
  filename = file_path.split('/')[-1]  # Extract the filename from the file path

  response['Content-Disposition'] = f'attachment; filename="{filename}"'

  return response

def auto_matching_DB_changer(request):
  customername = request.POST['customername']
  db = json.loads(request.POST["input"])
  res=generator.auto_matching_DB_changer(customername, db)
  return JsonResponse({ "message": "DB Updated!" })

@login_required
def live_doubleIgnore(request):
  matching_res = json.loads(request.POST["input"])
  customername = request.POST["customername"]
  terms = json.loads(request.POST["termOptions"])
  generator.live_save(matching_res, customername, terms)
  return JsonResponse({ "message": "hello" })

@login_required
def live_doubleUpdate(request):
  matching_res = json.loads(request.POST["input"])
  customername = request.POST["customername"]
  terms = json.loads(request.POST["termOptions"])

  res = generator.live_save(matching_res, customername, terms)
  generator.live_addition(res[0], res[1], res[2])

  return JsonResponse({ "message": "hello" })