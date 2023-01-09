Hello,

# Intro
This is my first project in python to scrap a webpage and store valuable data in a database.
The purpose of this project is educational only.


# Scope of the project
The script scraps the web real estate Zillow website for data to populate a listing database.


# Explaination of the script
The script is divided in 3 parts:

## Counter Zillow's use of CSS Dynamic tags
I noticed the website uses CSS Dynamic tags. This means that part of the _class name_ within a HTML tag changes frequently.
The first part of the script stores the latests class name of the tag by localising its index. This helps make the code robust agains Dynamic CSS. It can then run without having to change the _class name_ in the code everytime it is run.


## Scrap valuable data with Beautiful Soup 4
Next, once the script knows the latest class name of DOM tags, the script starts scrapping for data.

Thas is:
1. It collects the number total page to scrap (ie., `max_page`).
2. Next, it creates a list of url for every page up to `max_page` for the requested city and state.
3. Next, it iterates on every page and scrap the data that is then stored in list


### Create a Data Frame with Pandas and store data in a SQLite database
Eventually, the script creates a Data Frame with the various list of data scrapped.
If the database is not yet create, it creates it. Otherwise, it appends the freshly scrapped data to the database.


# Educational take-aways from this project
This project is my first major project in Python and first one in webscrapping.
I had fun sharpening my skills in Python, using the Terminal to run and debug code, use StackOverFlow and any other plateforme online to help me find solution to bugs, understand webscrapping and DOM.


# Ways to improve the code and follow-up of project.
- Optimize speed of the code (through classes and inheritances).
- Improve code readibility and documentation.
- Add a sys functionality to run code from commande line.
- Connect database to a visualization tool (eg., Tableau or PowerBi). Create some visualization.


# Contact
For any enquiry on this project, please contact me at jonathanverschaeve94@gmail.com.


Thanks for your interest,
Jonathan Verschaeve

