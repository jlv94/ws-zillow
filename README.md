# Disclaimer
The purpose of this project is purely educational.
There is no intention to frequently run the script, nor to store tremendous amount of data. There is no intention to sell the data or the script nor to make a profit out of this project.


# Scope of the project
In this project I learned how to:
* Write a python program to scrap webpage and with library such as Pandas, Request and BeautifulSoup
* Understand the concept of CSS Dynamics and counter this problem with a script that actually scrap the new name of css classes
* Clean scrapped data with Regex
* Create a new sqlite database, assign primary key and add the scrapped data to it
* Create example of SQL requests to get value out of the database
* Use create a repo in GitHub and use the Terminal to push the project



## Part I - Counter Zillow's use of CSS Dynamic tags
I noticed the website uses CSS Dynamic tags. This means that part of the _class name_ within a HTML tag can change frequently.
The first part of the script stores the latests _class name_ of the tag. To do so, I decided to localyse the index of the tag as the main structure stay the same over time. Doing so, I return and store in a list the (latest) value of a particular index.


## Part II - Scrap data with Beautiful Soup 4
The script reads the first page of a city we'd like to scrap property information with respect of the _class name_ gained in Part I. 

**Building a list of urls**
First, the script returns the max page listed on the site for the city in a variable `max_page`.
Then, it iteratively builds ulrl from page 1 up to `max_page` and stores it in a list (`url_list`). 
The structure of the url is: zillow.com/city-state/`x_p`, with `x` the page number.


**Scrap interatively**
Next, for every url the script scrap data, looking at the _class name_ found in Part I. Data is stored in appropriate list (ie., `data_id` stores the property ID ; `data_prices` stores the property price). This will set us up to build a data frame later on.


**Clean data within list**
Some data scraped need to be clean. For examples:
* The tag containing the information of the number of beds, bads and square foot is the same. Therefore the data therein is concatenate. The script first separate it (func `clean_data_info`) and then store the data in its corresponding list by slicing the items index within the list. That is, info of beds, bads and sqft are stored in the `data_info`list. After apply the function, we have a list of `[3 beds 4 bads 1,230 sqft, ...]`. I use the index position of every item within the list (which has always the same structure) to assign the number of beds to a `data_bed` list, and so on.
* Same schema applys to the `data_address` list which contains the full address. For analysis purposes, it may be usefule to split the street name to its zip code and city. The script iterates over every item of `data_address` list to build up new list such as `data_street`, `data_city` or `data_zip`.


**Building the data frame**
Next, the script creates a Data Frame using a list of columns (`df_columns`) and the various lists containing the data.


**Storing data in a local sqlite database**
Next, the script creates a sqlite database - if there is none already - and stores data from the dataframe in it. The sqlite database is created in the same folder as the python script.
The table name is `real_estate` and the primary key is set to be the property id number. 



## Ways to improve the project
Again, my goal was to learn the basics of webscraping and using sql to store data.
However, this is a first project and there is always room for improvement, such as to:
* Imprive speed and readability of the code, through code optimization, usage of classes and inheritances
* Add a sys functionality to run code from commande line
* Improve versatility of code to ensure any request of city scraping would actually work
* Write code to check the quality of any modification
* ...


# Contact
If you have any question or recommandation I'm all in to learn and share with others.
Please contact me at jonathanverschaeve94@gmail.com

Thanks for your interest



