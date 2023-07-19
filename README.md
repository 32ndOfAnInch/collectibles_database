# Collectible Items Database App
This is my final project of codeacademy.lt python course.
## Overview
The Collectible Items Database App is a Django-based web application that allows users to manage and catalog their collectible items, primarily coins, but also could be used for banknotes and possibly, for post stamps. It provides features for users to create, update, and search collectible items, as well as connect with other users through friend requests with the ability to see their databases.
## Key Features
* User registration and authentication
* Profile management with profile pictures
* Collectible item creation and management
* Search functionality to find specific items or users
  * Enhanced with fuzzy matching nlp libraries (spacy and fuzzywuzzy) to find closest matching items from given list from db
* Statistics
* Friend request system for connecting with other collectors
  * Ability to see a friend's collectible items
* Mobile-friendly interface
## Installation and Setup
1. Clone the repository: 
`git clone https://github.com/32ndOfAnInch/collectibles_database.git`
2. Navigate to the project directory
3. Install the project dependencies: 
`pip install -r requirements.txt`
4. Set up the database and create admin:
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py createsuperuser`
5. Start the development server:
`python manage.py runserver`
## License
GNU General Public License v3.0
##
Note that the project is still under construction, so, many changes can still happen.
Note 2: spacy library installation guide: https://spacy.io/usage
Note 3: I will soon add fixtures.json for item gradation systems and their values, to add fixtures to db, use command:
`python manage.py loaddata (name of file).json`
If your code editor doesn't catch spacy library, try to restart your code editor, it worked for me

Feel free to clone/fork