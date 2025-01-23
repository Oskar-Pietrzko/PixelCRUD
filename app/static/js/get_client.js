async function addNewNote() {
    const title = document.getElementById("newNoteTitle");
    const content = document.getElementById("newNoteContent");

    await fetch(`/api/client/${clientId}/note`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            title: title.value,
            content: content.value,
        })
    })

    window.location.reload()
}

function editNote(note_id) {
    const note = document.getElementById("note-" + note_id);
    const title = note.querySelector("#title");
    const titleText = title.innerHTML;

    const titleEditable = document.createElement("textarea");
    titleEditable.id = "title";
    titleEditable.classList.add("note__title");
    titleEditable.value = titleText;

    title.remove();
    note.prepend(titleEditable)

    const content = note.querySelector("#content");
    content.readOnly = false;

    const deleteButton = note.querySelector("#deleteButton");
    deleteButton.hidden = true;

    const editButton = note.querySelector("#editButton");
    editButton.hidden = true;

    const cancelButton = note.querySelector("#cancelButton");
    cancelButton.hidden = false;

    const saveButton = note.querySelector("#saveButton");
    saveButton.hidden = false;
}

function cancelNote(note_id) {
    const note = document.getElementById("note-" + note_id);
    const titleEditable = note.querySelector("#title");
    const titleText = titleEditable.value;

    const title = document.createElement("h2");
    title.id = "title";
    title.classList.add("note__title");
    title.innerHTML = titleText;

    titleEditable.remove();
    note.prepend(title)

    const content = note.querySelector("#content");
    content.readOnly = true;

    const deleteButton = note.querySelector("#deleteButton");
    deleteButton.hidden = false;

    const editButton = note.querySelector("#editButton");
    editButton.hidden = false;

    const cancelButton = note.querySelector("#cancelButton");
    cancelButton.hidden = true;

    const saveButton = note.querySelector("#saveButton");
    saveButton.hidden = true;
}

async function saveNote(note_id) {
    const note = document.getElementById("note-" + note_id);
    const title = note.querySelector("#title");
    const content = note.querySelector("#content");

    await fetch(`/api/client/${clientId}/note/` + note_id, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            title: title.value,
            content: content.value,
        })
    })

    window.location.reload()
}

async function deleteNote(note_id) {
    await fetch(`/api/client/${clientId}/note/` + note_id, {
        method: "DELETE",
    })

    window.location.reload()
}

async function uploadNote() {
    const input = document.getElementById("image");
    const file = input.files[0];

    const formData = new FormData();
    formData.append("note", file);

    await fetch(`/api/client/${clientId}/note/upload`, {
        method: "POST",
        body: formData,
    });

    window.location.reload()
}

async function deleteClient() {
    await fetch(`/api/client/${clientId}`, {
        method: "DELETE",
    })

    window.location.replace("/client")
}

async function editClient() {
    const client = (await (await fetch(`/api/client/${clientId}`)).json()).data

    document.getElementById("name").innerHTML = `<strong>Name: </strong><input type="text" id="newName" value="${client.name}" />`
    document.getElementById("surname").innerHTML = `<strong>Surname: </strong><input type="text" id="newSurname" value="${client.surname}" />`
    document.getElementById("email").innerHTML = `<strong>Email: </strong><input type="email" id="newEmail" value="${client.email}" />`

    document.getElementById("deleteClientButton").hidden = true;
    document.getElementById("editClientButton").hidden = true;
    document.getElementById("cancelClientButton").hidden = false;
    document.getElementById("saveClientButton").hidden = false;
}

function cancelClient() {
    fetchClient().then()

    document.getElementById("deleteClientButton").hidden = false;
    document.getElementById("editClientButton").hidden = false;
    document.getElementById("cancelClientButton").hidden = true;
    document.getElementById("saveClientButton").hidden = true;
}

async function saveClient() {
    const name = document.getElementById("newName").value;
    const surname = document.getElementById("newSurname").value;
    const email = document.getElementById("newEmail").value;

    let response = await (await fetch(`/api/client/${clientId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: name,
            surname: surname,
            email: email,
        }),
    })).json();


    if (!response.success) {
        alert(response.error);
    } else {
        window.location.reload()
    }
}

async function fetchClient() {
    const response = await fetch(`/api/client/${clientId}`);
    const client = await response.json();

    document.getElementById("id").innerHTML = `<strong>ID: </strong> ${client.data.id}`;
    document.getElementById("name").innerHTML = `<strong>Name: </strong> ${client.data.name}`;
    document.getElementById("surname").innerHTML = `<strong>Surname: </strong> ${client.data.surname}`;
    document.getElementById("email").innerHTML = `<strong>Email: </strong> ${client.data.email}`;
}

async function fetchNotes() {
    const response = await fetch(`/api/client/${clientId}/note`);
    const notes = await response.json();

    const main = document.getElementById("notes");

    if (notes.data.length === 0) {
        const note = document.createElement("section");
        note.classList.add("note");

        const title = document.createElement("h2");
        title.classList.add("note__title");
        title.innerText = "Client has no notes.";

        note.appendChild(title);
        main.appendChild(note);
    }

    notes.data.forEach((note) => {
        const section = document.createElement("section");
        section.classList.add("note");
        section.id = "note-" + note.id;

        const title = document.createElement("h2");
        title.id = "title";
        title.classList.add("note__title");
        title.innerHTML = note.title;

        const content = document.createElement("textarea");
        content.id = "content";
        content.classList.add("note__content");
        content.readOnly = true;
        content.innerHTML = note.content;

        const buttonContainer = document.createElement("div");
        buttonContainer.classList.add("note__actions");

        const deleteButton = document.createElement("button");
        deleteButton.id = "deleteButton";
        deleteButton.classList.add("btn");
        deleteButton.classList.add("btn-danger");
        deleteButton.innerHTML = "DELETE";
        deleteButton.addEventListener("click", () => deleteNote(note.id));

        const editButton = document.createElement("button");
        editButton.id = "editButton";
        editButton.classList.add("btn");
        editButton.classList.add("btn-primary");
        editButton.innerHTML = "EDIT";
        editButton.addEventListener("click", () => editNote(note.id));

        const cancelButton =document.createElement("button");
        cancelButton.id = "cancelButton";
        cancelButton.classList.add("btn");
        cancelButton.classList.add("btn-danger");
        cancelButton.innerHTML = "CANCEL";
        cancelButton.hidden = true;
        cancelButton.addEventListener("click", () => cancelNote(note.id));

        const saveButton = document.createElement("button");
        saveButton.id = "saveButton";
        saveButton.classList.add("btn");
        saveButton.classList.add("btn-success");
        saveButton.innerHTML = "SAVE";
        saveButton.hidden = true;
        saveButton.addEventListener("click", () => saveNote(note.id));


        buttonContainer.appendChild(deleteButton);
        buttonContainer.appendChild(editButton);
        buttonContainer.appendChild(cancelButton);
        buttonContainer.appendChild(saveButton);

        section.appendChild(title);
        section.appendChild(content);
        section.appendChild(buttonContainer);

        main.appendChild(section);
    });
}

document.addEventListener("DOMContentLoaded", function() {
    fetchClient().then();
    fetchNotes().then();

    document.getElementById("newNote").addEventListener("click", addNewNote);
    document.getElementById("uploadNote").addEventListener("click", uploadNote);
    document.getElementById("deleteClientButton").addEventListener("click", deleteClient);
    document.getElementById("editClientButton").addEventListener("click", editClient);
    document.getElementById("cancelClientButton").addEventListener("click", cancelClient);
    document.getElementById("saveClientButton").addEventListener("click", saveClient);
    document.getElementById("image").addEventListener("change", () => {
        document.getElementById("uploadNote").disabled = false;
    });
    document.getElementById("newNoteTitle").addEventListener("input", () => {
        document.getElementById("newNote").disabled = document.getElementById("newNoteTitle").value.length === 0;
    });
});
