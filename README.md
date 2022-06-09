# Learn!T
#### Video Demo:  <https://youtu.be/obEwlsnrD5U>
#### Description:
#### Overview
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

#### How to run locally

Python 3.0 installed on local machine is required.


#### Source folder tree

>src
> ┣ database
> ┃ ┣ learn!t.db
> ┃ ┗ schemas.txt
 ┣ static
 ┃ ┣ img
 ┃ ┃ ┗ favicon.ico
 ┃ ┣ js
 ┃ ┃ ┣ account.js
 ┃ ┃ ┣ changepassword.js
 ┃ ┃ ┣ controlpanel.js
 ┃ ┃ ┣ learning-paths.js
 ┃ ┃ ┣ new_path.js
 ┃ ┃ ┣ path.js
 ┃ ┃ ┣ recover.js
 ┃ ┃ ┗ register.js
 ┃ ┗ styles.css
 ┣ templates
 ┃ ┣ about.html
 ┃ ┣ account.html
 ┃ ┣ changepassword.html
 ┃ ┣ controlpanel.html
 ┃ ┣ errorpage.html
 ┃ ┣ layout.html
 ┃ ┣ learning-paths.html
 ┃ ┣ login.html
 ┃ ┣ new_path.html
 ┃ ┣ path.html
 ┃ ┣ preview.html
 ┃ ┣ privacy.html
 ┃ ┣ recover.html
 ┃ ┣ register.html
 ┃ ┗ register_success.html
 ┣ __pycache__
 ┃ ┣ app.cpython-310.pyc
 ┃ ┣ control_panel.cpython-310.pyc
 ┃ ┣ helpers.cpython-310.pyc
 ┃ ┗ mail_service.cpython-310.pyc
 ┣ .env
 ┣ app.py
 ┣ helpers.py
 ┗ mail_service.py