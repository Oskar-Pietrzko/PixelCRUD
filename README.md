<div id="readme-top" align="center">
    <h3 align="center">PixelCRUD</h3>
</div>

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
    </ol>
</details>

## About The Project
This repository contains a CRUD (Create, Read, Update, Delete) application enhanced with OCR (Optical Character Recognition) functionality. The project was developed as part of a vocational internship at Pixel.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Developers

* Oskar Pietrzko
* Klaudiusz Pielaszkiewicz
* Szymon Podlasiak
* Stanisław Pellowski-Zawistowski
* Kacper Sawicki
* Paweł Król

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
* ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
* ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Tested On

* ![Windows 11](https://img.shields.io/badge/Windows%2011-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)
* ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
* ![Brave](https://img.shields.io/badge/Brave-FB542B?style=for-the-badge&logo=Brave&logoColor=white)
* ![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Routes

### POST /api/user : Create New User
Request Body:
* name (string, required): The name of the user.
* surname (string, required): The surname of the user.
* email (string, required): The email of the user.

Response Body:
* success ()
* data ()
  * User data

### GET /api/user : Get List of Users
The GET request to /api/user endpoint retrieves user information. The response is a JSON object with a success key indicating the status of the request, and a data array containing user details. Each user object in the data array includes id, name, surname, and email keys, all of which are strings.

### GET /api/user/\<userid> : Get User
The API endpoint retrieves user information based on the provided user ID. The response is in JSON format.\
Response Body:
* success ()
* data ()
    * User data

### PUT /api/user/\<userid> : Update User
The PUT request to /api/user/\<userid> endpoint allows you to change information about the user of the provided user ID. The response it gives is the new, changed user information in JSON format.

Request Body:
* name (string, optional): The name of the user.
* surname (string, optional): The surname of the user.
* email (string, optional): The new email of the user.

Response Body:
* success ()
* data ()
    * User data

### DELETE /api/user/\<userid> : Delete User
The DELETE request to /api/user/\<userid> endpoint deletes the user of the provided user ID. The response is a JSON object with a success key indicating the status of the request, and an empty data object.




### POST /api/user/\<userid>/note : Create note
The POST request to /api/user/\<userid>/note endpoint creates a note with specified title and contents.

Request body:
* title(string, required)
* content(string, required)

Response body:
* success ()
* data ()
  * title()
  * content()

### POST /api/user/\<userid>/note/upload : Create a note from a file
The POST request to /api/user/\<userid>/note/upload endpoint creates a text note from a file that has been sent.

Request body:
* note(file, required)

Response body:
* success ()
* data ()
    * title()
    * content()
