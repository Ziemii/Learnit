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

In response to queries, the server renders the appropriate template, often querying the database for the necessary information.

The application supports user accounts with essentials such as encrypted passwords, encrypted sessions, ability to change password, password reset service and account deletion.

Logged in users can add new tracks, rate tracks and add favorite ones to bookmarks.

# How to run locally

Python 3.0 installed on local machine is required.


# Source folder tree

## src

* [database/](.\src\database) *Database folder with demo database and text file showing used schemas*
  * [learn!t.db](.\src\database\learn!t.db)
  * [schemas.txt](.\src\database\schemas.txt)
* [static/](.\src\static) *All static files*
  * [img/](.\src\static\img)
    * [favicon.ico](.\src\static\img\favicon.ico)
  * [js/](.\src\static\js) *JS Scripts supporting html files with the same name*
    * [account.js](.\src\static\js\account.js)
    * [changepassword.js](.\src\static\js\changepassword.js)
    * [controlpanel.js](.\src\static\js\controlpanel.js)
    * [learning-paths.js](.\src\static\js\learning-paths.js)
    * [new_path.js](.\src\static\js\new_path.js)
    * [path.js](.\src\static\js\path.js)
    * [recover.js](.\src\static\js\recover.js)
    * [register.js](.\src\static\js\register.js)
  * [styles.css](.\src\static\styles.css)
* [templates/](.\src\templates) *Html templates used by Flask when constructing view*
  * [about.html](.\src\templates\about.html)
  * [account.html](.\src\templates\account.html)
  * [changepassword.html](.\src\templates\changepassword.html)
  * [controlpanel.html](.\src\templates\controlpanel.html)
  * [errorpage.html](.\src\templates\errorpage.html)
  * [layout.html](.\src\templates\layout.html)
  * [learning-paths.html](.\src\templates\learning-paths.html)
  * [login.html](.\src\templates\login.html)
  * [new_path.html](.\src\templates\new_path.html)
  * [path.html](.\src\templates\path.html)
  * [preview.html](.\src\templates\preview.html)
  * [privacy.html](.\src\templates\privacy.html)
  * [recover.html](.\src\templates\recover.html)
  * [register.html](.\src\templates\register.html)
  * [register_success.html](.\src\templates\register_success.html)
* [.env](.\src\.env) *I provided some credentials to make this functional out of the box*
* [app.py](.\src\app.py) *Main Flask application file, all requests are processed here*
* [helpers.py](.\src\helpers.py) >*Decorators definitions*
* [mail_service.py](.\src\mail_service.py)
