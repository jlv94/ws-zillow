'''
ws-zillow

Educational webscraping project
Author: Jonathan Verschaeve
Contact: jonathanverschaeve94@gmail.com
'''

#Library
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup
import requests
import re


##### PART I #######

'''
This scrip will allow us to scrap the class names. Zillow uses Dynamic Generated CSS class which makes it difficult to rerun the scrip if using fixed class name.
'''

#Create a standard url
url = "https://www.zillow.com/calgary-ab/1_p"
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

#Parse page content
page = requests.get(url, headers=header)
page_content = BeautifulSoup(page.content, "html.parser")


#Find all the tags used in the html page

## Tags ul within the fixed div id "grid_search-results" (main) contains all listing (in li tags).
## We'll first get the ul class name.
ul_class = [' '.join(i) for i in [page_content.find("div", class_="result-list-container").find("ul")["class"]]]

## Next we'll get the unique li tags class name within ul tags
li_class = [' '.join(i) for i in [page_content.find("ul", class_=ul_class).find("li")["class"]]]

## Get a list of all div class name within a li tags
### Get first div tag
div_class = [' '.join(i) for i in [page_content.find("li", class_=li_class).find("div")["class"]]]

### Get a list of all tag within the first div Tag. This contains all the containers where our data will be scrapped.
div_all = str(page_content.find("div", {"class":div_class}))
div_all = re.sub("><", '>***<', div_all)
div_all = div_all.split("***")


### Next, we'll have to attribute the class name of the data we want to scrap to the proper tag from within the list generated.
'''
We'll be scrapping these data:
"type": type of property 
"price": price asked
"address": complete adress
"info": beds, bads and sqft
"agency": the agency listing the property
"property_url": the url of property,
"image_1_url": the url property first image

The rest of the data will be computed later on, through the data scrapped here.
'''
### Property ID is located in the only article tag"
class_id = [' '.join(i) for i in [page_content.find("li", class_=li_class).find("article")["class"]]][0]

### Url of property and property Address are located within class containing 'property-card-link'
class_1 = [div_all.index(i) for i in div_all if 'data-test="property-card-link"' in i][0]
class_1 = div_all[class_1] 
class_1 = class_1[class_1.find("class")+7:class_1.find('data-test=')-2]


### Prices of property is located within the span tag "property-card-price", first child of div class containing "style-property-card-data-area"
class_prices = [div_all.index(i) for i in div_all if 'data-test="property-card-price"' in i][0]-1
class_prices = div_all[class_prices]
class_prices = class_prices[class_prices.find("class")+7:class_prices.find('">')]

### Agency is located within the div tag which comes right after <a> tag containing data-test="property-card-link" (DOM + 3)
class_agency = [div_all.index(i) for i in div_all if 'data-test="property-card-link"' in i][0]+3
class_agency = div_all[class_agency]
class_agency = class_agency[class_agency.find("class")+7:class_agency.find('">')]


### Property info is located within a div right after span tag "property-card-price" (DOM + 3)
class_info = [div_all.index(i) for i in div_all if 'data-test="property-card-price"' in i][0]+2
class_info = div_all[class_info]
class_info = class_info[class_info.find("class")+7:class_info.find('">')]


### Url of property picture is located in a img tag under a div tag starting with 'class="StyledPropertyCardPhoto-"' (DOM + 1)
class_pic = [div_all.index(i) for i in div_all if 'StyledPropertyCardPhoto-' in i][0]+1
class_pic = div_all[class_pic]
class_pic = class_pic[class_pic.find("class")+7:class_pic.find('" src')]


#################           #######################





########### PART II #############


#Build Zillow url to scrap
city = "Kamloops"
state = "BC"

url_std = "https://www.zillow.com/" + city.lower() + "-" + state.lower() + "/1_p"
header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}


#Get max number of pages to scrap to create url index
page_url_std = requests.get(url_std, headers=header)
url_std_content = BeautifulSoup(page_url_std.content, "html.parser")

total_page = url_std_content.find(class_="Text-c11n-8-81-1__sc-aiai24-0 cOjNXl")
total_page = total_page.get_text().split()
max_page = int(total_page.pop())

#Build list of url for all pages
url_list = []
p = 1

for p in range (1, max_page + 1, 1):
	url_list.append("https://www.zillow.com/" + city.lower() + "-" + state.lower() + "/" + str(p) + "_p")

#Create empty list to store data by variable
data_id = []
scrip_tags = []
data_prices = []
data_address = []
data_agency = []
data_info = []
data_url = []
data_image = []

#Loop through the whole url list build
for url in url_list:
	url_request = requests.get(url, headers=header)
	url_content = BeautifulSoup(url_request.content, "html.parser")

#Loop through all url and find list of real estate ("li") from the class that store data to scrap
	for listing in url_content.find_all("li", class_=li_class):

		for property_id in listing.find_all("article", class_=class_id):
			if property_id is not None:
				property_id = property_id.get("id")
				property_id = re.sub("zpid_", "", property_id)
				data_id.append(property_id)
			else:
				continue

		for prices in listing.find_all(class_=class_prices):
			'''
			Loop and store the price of property in a list in its text value.
			'''
			if prices is not None:
				prices = prices.text
				prices = re.sub("[C$]", "", prices)
				prices = re.sub(",", "", prices)
				data_prices.append(prices)
			else:
				continue

		for address in listing.find_all(class_=class_1):
			'''
			Store full address of property.
			Later on, we'll have to clean street address from zipcode and city.
			'''
			if address is not None:
				data_address.append(address.text)
			else:
				continue

		for agency in listing.find_all(class_=class_agency):
			'''
			Store agency name who posted the ad on Zillow.
			'''
			if agency is not None:
				data_agency.append(agency.text)
			else:
				continue

		for info in listing.find_all(class_=class_info):
			if info is not None:
				data_info.append(info.text)

		for url_property in listing.find_all("a", class_=class_1):
			'''
			Get property unique url.
			Later on, we'll extract from the url the property ID and use it as Primary Key.
			'''
			if url_property is not None:
				data_url.append(url_property.get("href"))
			else:
				continue

		for url_image in listing.find_all("img", class_=class_pic):
			if url_image is not None:
				data_image.append(url_image.get("src"))
			else:
				continue

#Clean data_info list and ventilate information for number of beds, bads and sqft towards appropriate list
##First let's create a function to only keep digits and clean undesired pattern
def clean_data_info(list_to_clean):
	pattern_to_remove = "[a-z,]"
	pattern_to_replace = "--"
	list_to_clean = [i.replace("bds", "beds ") for i in list_to_clean]
	list_to_clean = [i.replace("bd", "beds ") for i in list_to_clean]
	list_to_clean = [i.replace("ba", "bads ") for i in list_to_clean]
	list_to_clean = [i.replace("bas", "bads ") for i in list_to_clean]
	return list_to_clean

##Apply this function to data_info list
'''
First position is for number of bedrooms
Second position is for numbers of badrooms
Third position is property sqft
Fourht position is the property type
'''
data_info = clean_data_info(data_info)

##Next, interate through this index to create 3 new lists (ie., number of bedrooms, number of badrooms & property sqft)
data_beds = []
data_bads = []
data_sqft = []
data_types = []

for bed in data_info:
	bed = bed[0:bed.find("beds")-1]
	data_beds.append(bed)

for bad in data_info:
	bad = bad[bad.find("beds")+5:bad.find("bads")-1]
	data_bads.append(bad)

for sqft in data_info:
	sqft = sqft[sqft.find("bads")+5:sqft.find("sqft")-1]
	sqft = re.sub(",", "", sqft)
	data_sqft.append(sqft)

for types in data_info:
	types = types[types.find("-")+2:]
	data_types.append(types)

# for lots in data_types:
# 	'''
# 	Clean types lots in bed and bads variable.
# 	'''
# 	if lots == "Lot / Land for sale":
# 		for lots in data_beds:
# 			lots = 0
# 			data_beds.append(lots)
		
# 		for lots in data_bads:
# 			lots = 0
# 			data_bads.append(lots)
		
# 		for lots in data_sqft:
# 			lots = lots[:lots.find("sqft")-1]
# 			lots = re.sub(",", "", lots)
# 			data_sqft.append(lots)
# 	else :
# 		continue

#Clean address for further analysis
data_street = []
data_city = []
data_state = []
data_zip = []

for street in data_address:
	street = street[0:street.find(",")]
	data_street.append(street)

for city in data_address:
	city = city[city.find(",")+2:city.find(",", city.find(",")+1)]
	data_city.append(city)

for state in data_address:
	state = state[state.find(",", state.find(",")+2)+2:state.find(" ", state.find(",")+2)+3]
	data_state.append(state)

for zip_code in data_address:
	zip_code = zip_code[zip_code.find(",", zip_code.find(",")+2)+2:]
	zip_code = zip_code[3:]
	data_zip.append(zip_code)

#Dataframe
df_columns=["id", "type", "price", "address", "beds", "bads", "sqft", "street", "city", "state", "zip_code","agency", "property_url", "image_1_url"]
df = pd.DataFrame(list(zip(data_id, data_types, data_prices, data_address, data_beds, data_bads, data_sqft, data_street, data_city, data_state, \
							data_zip, data_agency, data_url, data_image)), columns=df_columns)

#Drop duplicated listing
df = df.drop_duplicates(subset=["id"])

#Database connection
db_conn = sqlite3.connect("real_estate.db")
db_cursor = db_conn.cursor()

#Create table if it does not already exist
create_table = ("CREATE TABLE IF NOT EXISTS real_estate(id TEXT PRIMARY KEY NOT NULL UNIQUE, \
				type TEXT, price INT, address TEXT, beds INT, bads INT, sqft INT, street TEXT, city TEXT, state TEXT, \
				zip_code TEXT, agency TEXT, property_url TEXT, image_1_url TEXT)")

db_cursor.execute(create_table)

#Insert new data to data base
df.to_sql("real_estate", con=db_conn, if_exists="append", index=False)

db_conn.commit()
db_conn.close()

print("Script is done for ", city)