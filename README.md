<div id="readme-top" align="center">
    <a href="https://github.com/Oskar-Pietrzko/PixelCRUD">
        <img src=".github/images/logo.svg" alt="Logo" width="80" height="80" />
    </a>
    <h3 align="center">PixelCRUD</h3>
</div>

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
                <li><a href="#tested-on">Tested On</a></li>
            </ul>
        </li>
        <li>
            <a href="#routes">Routes</a>
            <ul>
                <li><a href="#client-routes">Client</a></li>
                <li><a href="#note-routes">Note</a></li>
            </ul>
        </li>
    </ol>
</details>

## About The Project
This repository contains a CRUD (Create, Read, Update, Delete) application enhanced with OCR (Optical Character Recognition) functionality. The project was developed as part of a vocational internship at Pixel.

### Developers
- Oskar Pietrzko  
- Klaudiusz Pielaszkiewicz  
- Szymon Podlasiak  
- Stanisław Pellowski-Zawistowski  
- Kacper Sawicki  
- Paweł Król  

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
- ![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Tested On
- ![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
- ![Brave](https://img.shields.io/badge/Brave-FB542B?style=for-the-badge&logo=Brave&logoColor=white)
- ![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

---

## Routes

### Client Routes

#### POST /api/client: Create New Client  
**Request Body:**  
- `name` (string, required): The name of the client.  
- `surname` (string, required): The surname of the client.  
- `email` (string, required): The email of the client.  

**Response Body:**  
- `success` (boolean)  
- `data` (object): Contains the created client data.

---

#### GET /api/client: Get List of clients  
Returns a list of all clients.  

**Response Body:**  
- `success` (boolean)  
- `data` (array): Each client object contains:  
  - `id` (string)  
  - `name` (string)  
  - `surname` (string)  
  - `email` (string)  

---

#### GET /api/client/\<client_id>: Get client  
Retrieves client information by ID.  

**Response Body:**  
- `success` (boolean)  
- `data` (object): Contains client data.

---

#### PUT /api/client/\<client_id>: Update client  
Updates client information by ID.  

**Request Body:**  
- `name` (string, optional): New name of the client.  
- `surname` (string, optional): New surname of the client.  
- `email` (string, optional): New email of the client.  

**Response Body:**  
- `success` (boolean)  
- `data` (object): Updated client data.

---

#### DELETE /api/client/\<client_id>: Delete client  
Deletes a client by ID.  

**Response Body:**  
- `success` (boolean)  
  - `data` (object): Empty object.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Note Routes

#### POST /api/client/\<client_id>/note: Create Note  
Creates a new note for a specific client.  

**Request Body:**  
- `title` (string, required): The title of the note.  
- `content` (string, optional): The content of the note.  

**Response Body:**  
- `success` (boolean)  
- `data` (object):  
  - `title` (string)  
  - `content` (string)  

---

#### POST /api/client/\<client_id>/note/upload: Create Note from File  
Creates a text note for a client from an uploaded file.  

**Request Body:**  
- `note` (file, required): The file containing the note.  

**Response Body:**  
- `success` (boolean)  
- `data` (object):  
  - `title` (string)  
  - `content` (string)  

---

#### GET /api/client/\<client_id>/note: Get All Notes  
Retrieves all notes for a specific client.  

---

#### GET /api/client/\<client_id>/note/\<note_id>: Get Note  
Retrieves a specific note by its ID.  

**Note:** The `<note_id>` is global across all clients. For example, if Client 1 creates a note with `note_id = 1`, client 2's first note will have `note_id = 2`.

---

#### PUT /api/client/\<client_id>/note/\<note_id>: Update Note  
Updates a specific note for a client.  

**Request Body:**  
- `title` (string, optional): Updated title of the note.  
- `content` (string, optional): Updated content of the note.  

**Response Body:**  
- `success` (boolean)  
- `data` (object):  
  - `title` (string)  
  - `content` (string)  

---

#### DELETE /api/client/\<client_id>/note/\<note_id>: Delete Note  
Deletes a specific note by its ID for a client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
