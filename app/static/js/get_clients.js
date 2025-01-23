async function fetchClients() {
    const response = await fetch("/api/client");
    const clients = await response.json();

    const table = document.getElementById("clients");
    const tbody = document.createElement("tbody");

    clients.data.forEach((client) => {
        const row = document.createElement("tr");

        row.innerHTML = `
                        <td><a href="/client/${client.id}">${client.id}</a></td>
                        <td>${client.name}</td>
                        <td>${client.surname}</td>
                        <td>${client.email}</td>
                    `
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
}

async function addClient() {
    const response = await (await fetch("/api/client", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            name: document.getElementById("name").value,
            surname: document.getElementById("surname").value,
            email: document.getElementById("email").value,
        })
    })).json();

    if (!response.success) {
        alert(response.error);
    } else {
        window.location.reload()
    }
}

document.addEventListener("DOMContentLoaded", function () {
    fetchClients();
    document.getElementById("buttonAddClient").addEventListener("click", addClient)

    document.querySelectorAll(".form__input input").forEach((input) => {
        input.addEventListener("input", function() {
            document.getElementById("buttonAddClient").disabled = false;

            document.querySelectorAll(".form__input input").forEach((input) => {
                document.getElementById("buttonAddClient").disabled = input.value === "";
            });
        });
    });
});
