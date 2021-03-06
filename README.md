# Learn!T
#### Video Demo:  <https://youtu.be/obEwlsnrD5U>
#### Description:
# Overview
>This website was created to share knowledge and skills as well as a way to master knowledge and skills, hence the concept of learning paths.
>A learning path should be on a specific topic, it may be summarized in one or two sentences, and it should contain references to the materials needed to complete it, that is, to get to know the topic.
>Learning paths are available to every visitor. Visitors can view the contents of the path, but cannot vote, add paths to favorites, or create new paths.
>The above privileges are available to those who have an account. An account is easy to set up and the only information we collect is an e-mail address and it is not shared with anyone.
>Anyone with an account can add new paths, which, after verifying the content, will be added to those visible under the learning paths. The path is not judged for any reason other than containing illegal content.
>Now come on, share your knowledge.

The assumption of the project was to create a web application enabling the exchange of knowledge and skills in the form of learning paths.
The project was built mainly using the python Flask framework communicating with the SQLite database.
The frontend part is HTML with bootstrap and jinja, and interactivity is supported by JavaScript with the addition of jQuery.
Communication with the backend layer takes place using HTTP requests sent by the browser using forms or direct requests.
In response to queries, the server responds with appropriate template or HTTP code, often querying the database for the necessary information in the process.
The application supports user accounts with essentials such as encrypted passwords, encrypted sessions, ability to change password, password reset service and account deletion.
Logged in users can add new tracks, rate tracks and add favorite ones to bookmarks.

# How to run locally

Python 3.10 installed on local machine is required. [Download](https://www.python.org/downloads/)

### Download or clone repository

#### Archive download

[Download](https://github.com/Ziemii/Learnit/archive/refs/heads/main.zip) main branch ZIP file 

#### Git

When using git I recommend using below command as it clones only main branch. I got other one where code is integrated with Heroku and it cannot be run locally. 
```
git clone -b main --single-branch https://github.com/Ziemii/Learnit.git
```

I also recommend using the python virtual environment.

### Create an environment

macOS/linux:
```
$ cd Learnit
$ python3 -m venv venv
```
Windows:
```
> cd Learnit
> py -3 -m venv venv
```

### Activate environment
macOS/linux:
```
$ . venv/bin/activate
```
Windows:
```
> venv\Scripts\activate
```
Your shell prompt will change to show the name of the activated environment.

### Install all dependencies
In root folder(Learnit):
```
$ pip install -r requirements.txt
```

### Run Flask App
```
$ cd src
$ flask run
```

### App should be available at http://127.0.0.1:5000, if you notice that this address is different, please adjust .env variable

# Project File Tree

* [src/](src/)
  * [database/](src/database) *Database folder with demo database and text file showing used schemas*
    * [learn!t.db](src/database/learn!t.db)
    * [schemas.txt](src/database/schemas.txt)
  * [static/](src/static) *All static files*
    * [img/](src/static/img)
      * [favicon.ico](src/static/img/favicon.ico)
    * [js/](src/static/js) *JS Scripts supporting interactivity*
      * [account.js](src/static/js/account.js)
      * [changepassword.js](src/static/js/changepassword.js)
      * [controlpanel.js](src/static/js/controlpanel.js)
      * [learning-paths.js](src/static/js/learning-paths.js)
      * [new_path.js](src/static/js/new_path.js)
      * [path.js](src/static/js/path.js)
      * [recover.js](src/static/js/recover.js)
      * [register.js](src/static/js/register.js)
    * [styles.css](src/static/styles.css)
  * [templates/](src/templates) *Html templates used by Flask when constructing view*
    * [about.html](src/templates/about.html)
    * [account.html](src/templates/account.html)
    * [changepassword.html](src/templates/changepassword.html)
    * [controlpanel.html](src/templates/controlpanel.html)
    * [errorpage.html](src/templates/errorpage.html)
    * [layout.html](src/templates/layout.html) *Main layout within which other pages are built*
    * [learning-paths.html](src/templates/learning-paths.html)
    * [login.html](src/templates/login.html)
    * [new_path.html](src/templates/new_path.html)
    * [path.html](src/templates/path.html)
    * [preview.html](src/templates/preview.html)
    * [privacy.html](src/templates/privacy.html)
    * [recover.html](src/templates/recover.html)
    * [register.html](src/templates/register.html)
    * [register_success.html](src/templates/register_success.html)
  * [.env](src/.env) *I provided some credentials to make this functional out of the box*
  * [app.py](src/app.py) *Main Flask application file, all requests are processed here*
  * [helpers.py](src/helpers.py) *Decorators definitions, helping restricting some routes only for logged users*
  * [mail_service.py](src/mail_service.py) *Account activation and password reset mail templates and service*
* [README.md](README.md)
* [requirements.txt](requirements.txt) *List of packages required to run this application*



# Usage 

After visiting the application address, a list of active learning paths is displayed. The list is in the form of interactive cards containing basic information about a given path.
It shows the track title, a list of interactive tags, an abstract, and the current user rating.

All visitors can view active paths.The results can be filtered using path name or tag. Additionally, the results can be sorted alphabetically or based on the rating, both by descending and ascending order.
However, in order to be able to take advantage of additional functionalities such as creating your own paths, adding paths to your favorites or evaluating them, an account is required.

An account can be created by visiting the login screen using the "Login" button in the upper right corner of the application screen or by expanding the list menu if the responsive rule was activated by the size of our screen. Below the login form there is a link to the registration form, as well as one for resetting the password on an existing account.

When creating an account, please provide your login, password and e-mail address.
E-mail is collected only to support the functionality of the application and is not used anywhere else. After completing the registration form and accepting the privacy notice, an email with an account activation link is sent to the address provided.

The application composes an email with the appropriate activation code, unique for each user, and sends it using the SMTP protocol using credentials from the ".env" file.
For the purposes of this version and to ensure the out of the box works, I decided to provide an .env file with necessary informations filled in.

After visiting the activation link, we can log in.
Logging in takes us back to the list of active learning paths where we can add a new path by selecting the "Add +" button as well as vote and bookmark the paths.

The form for adding a new track requires a title, brief summary, filling in the tag field and the body of the track itself.
As part of the form, I put a simple text editor that allows to format the text with a few standard tools and add external images, links and videos.

After adding a new path, it is saved in the database as inactive until the content is verified and approved or rejected in the admin control panel. Before activation, the path is already visible under user "Submission" tab, it can be previewed but will not be visible on the list of learning paths.

The account site allows you to view and manage your bookmarks and submitted paths. In addition, it gives access to information about the account under the "My account" tab and includes functionalities such as changing the password or deleting the account along with the submitted content.

For presentation purposes, access to the control panel is possible at the address:

``` http://127.0.0.1:5000/controlpanel ``` and the password is ``` 123 ``` 

The control panel allows you to accept or reject submissions. It is worth bearing in mind that the page does not refresh automatically after making the verdict.

# Thoughts and notes

SQLite was the database of choice for the local variant due to the ease of implementation and the ability to painlessly share the database along with the code. This choice is not appropriate if the application would be available online, in which case my choice would be an online hosted PostgreSQL database.

User sessions are not permanent and the session itself is encrypted.

Input validation is client-side. The server mainly checks if the parameters sent, or the results returned by the database using these parameters, are not Null.

Sorting the results was solved by relying on appropriately structured database queries so that the returned results were already in the order requested by the client. This seems to me to be a better solution than implementing an inside application sorting algorithm that works on unsorted results from the database for each request.

Pagination of the results is done by calculating, depending on the number of the desired page, the offset by which the database index should be moved and limiting the returned results to the number of results set as the maximum number of results per page.
