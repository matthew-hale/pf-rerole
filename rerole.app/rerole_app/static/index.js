"use strict";

var hostname = "http://localhost:5000";
var base_api_url = `${hostname}/api/v0`;
var site_characters_url = `${hostname}/characters`;

window.onload = populate_list;

async function populate_list() {
    const dom_character_list = document.getElementById("character-list");
    const character_list = await get_character_list()
    for (const c of character_list) {
        let id = c.id;
        let name = c.name ? c.name : "Unnamed character";

        let c_div = document.createElement("div");
        c_div.setAttribute("class", "character");
        c_div.setAttribute("id", id);

        let h3 = document.createElement("h3");
        h3.innerHTML = name;
        c_div.appendChild(h3);

        let buttons = document.createElement("div");
        buttons.setAttribute("class", "buttons");
        c_div.appendChild(buttons);

        let link = document.createElement("a");
        link.setAttribute("href", `${site_characters_url}/${id}`);
        link.innerHTML = "View";
        buttons.appendChild(link);

        let delete_button = document.createElement("button");
        delete_button.setAttribute("onclick", "delete_character(this)");
        delete_button.setAttribute("type", "button");
        delete_button.setAttribute("class", "delete");
        delete_button.innerHTML = "Delete";
        buttons.appendChild(delete_button);

        dom_character_list.appendChild(c_div);
    }
}

function delete_character(obj) {
    const buttons = obj.parentNode;
    const c_div = buttons.parentNode;
    const id = c_div.getAttribute("id");
    if (!confirm("Are you sure you wish to delete this character? This action cannot be undone.")) {
        return
    }
    try {
        fetch(`${base_api_url}/characters/${id}`, {
            method: "DELETE",
            headers: {
                Authorization: get_authorization_header(),
            },
            credentials: "same-origin",
        })
            .then((res) => {
                if (res.status == 401) {
                    logout();
                }
                if (res.ok) {
                    c_div.remove();
                }
            });
    } catch (error) {
        alert("An error occurred while deleting your character.");
        console.error(error);
    }
}

function create_character() {
    try {
        let data;
        fetch(`${base_api_url}/characters`, {
            method: "POST",
            headers: {
                Authorization: get_authorization_header(),
            },
            credentials: "same-origin"
        })
            .then((res) => {
                if (res.status == 401) {
                    logout();
                }
                return res.json()
            })
            .then((json) => {
                data = json;
                window.location.href = `${site_characters_url}/${data.id}`;
            });
    } catch (error) {
        alert("An error occurred while creating a new character.");
        console.error(error);
        window.location.reload();
    }
}

async function get_character_list() {
    const endpoint = `${base_api_url}/characters`;
    let headers = {
        Authorization: get_authorization_header()
    }
    return await fetch(endpoint, {
        method: "GET",
        headers: headers,
        credentials: "same-origin"
    })
        .then((res) => {
            if (res.status == 401) {
                throw "401";
            }
            return res.json();
        })
        .catch((err) => {
            logout();
        });
}

function logout() {
    let token = window.localStorage.getItem("token");
    fetch(`${base_api_url}/logout`, {
        method: "POST",
        headers: {
            Authorization: get_authorization_header(),
        },
        credentials: "same-origin",
    })
        .then((res) => {
            console.log(res);
        })
        .finally(() => {
            window.localStorage.clear();
            window.location.replace(`${hostname}/logout`);
        });
}

function get_authorization_header() {
    let token = window.localStorage.getItem("token");
    let value = `Bearer ${token}`;
    return value;
}
