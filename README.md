# FlashCards-WebAPI

## Distinctiveness and Complexity: 
This web application is my capstone submission for **CS50’s Web Programming with Python and JavaScript**. Built using the **Django Web Framework**, **SQLite**, and **Bootstrap**, this is a FlashCards application for learners of memory-intensive subjects such as foreign languages. 

The application includes these main features:

1. User registration: Users can register for an account that will save information such as study sets they have created.

2. Creation of study sets: Users can create a study set that has a title, a description, and a collection of cards. Each card contains a term and a definition. For ease of saving longer lists of terms and definitions, users can choose the `Save & Add Cards via CSV/Excel file` option to upload a CSV or Excel files containing the terms and definitions to be saved. Note that the user must have already created a study set with at least a name to choose this option.

3. Editing of study sets: Users can edit the name and description of a set, or add, edit and delete cards in an existing set. The set can also be permanently deleted from the user's account and the database through the `delete` button on the set page.

4. Studying a study set: Users can `study` an existing set (i.e. enter the correct term for each definition shown on the page until they have completed all cards in the set).

5. Testing a study set: Users can `test` themselves on an existing set (i.e. enter the term for each definition shown on the page and receive a final grade based on their accuracy).

6. Adding/Removing a study set from collection: Users can save any study set from another user to their collection to study and test. Saved sets can also be removed from their collection. Note that users who are not owner of a set cannot edit the set's content. 

7. Viewing a user's profile: View the user's information, such as date of account creation, last log-in date, and all study sets this user has created.

Other funtionalities:
- Copying the link to a set/user onto the clipboard to share with another user
- Checking information of a set, such as number of cards and date of creation
- Deleting a user's account

8. Mobile-responsiveness: This application's user interface will change accross different devices' screen sizes for ease of use. Some images may not be shown on a smaller screen. 

## Important folders and files in this directory:

`requirements.txt`: Important packages and libaries to run this application.

`db.sqlite3`: The SQLite database for this application.

In the `flashcards` sub-directory:

`static/flashcards`: Contains static files for this application, including:
- Media files (e.g. favicon)
- Template CSV/Excel files for set creation (`sample.csv` & `sample.xlsx`)
- Front-end Javascript and CSS code (`script.js` & `styles.css`)

`templates/flashcards`: Contains HTML templates for this application.
- `layout.html`: HTML layout for other HTML files
- `error.html`: Custom error messages
- `login.html`: User log-in page
- `register.html`: User registration page
- `index.html`: Index page
- `create.html`, `add-cards-csv.html`: Study set creation (manual & via file upload)
- `set.html`, `study.html`, `test.html`: View, study, test the content of a set
- `test.html`: Rendering test results

## How to run this application:
1. In your terminal, `cd` to this directory
2. Run `pip install -r -requirements.txt` (Windows) or `pip3 install -r -requirements.txt` (Linux)
3. Run `python manage.py runserver`

## Additional information:
Possible improvements to the project:
- Editing a user's account (e.g. edit username/password)
- Storing test scores and user's actions/commitment

Possible frameworks/technologies to integrate:
- Docker & PostGres (back-end)
- React (front-end)