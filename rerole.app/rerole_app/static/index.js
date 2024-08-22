var hostname = "http://localhost:5000";
var base_api_url = `${hostname}/api/v0`;
var site_characters_url = `${hostname}/characters`;

window.onload = populate_list;

async function populate_list() {
    dom_character_list = document.getElementById("character-list");
    try {
        const character_list = await get_character_list();
        console.log("success");
        for (const c of character_list) {
            id = c.id;
            name = c.name ? c.name : "Unnamed"; 

            c_div = document.createElement("div");
            c_div.setAttribute("class", "character");

            p = document.createElement("p");
            p.innerHTML = name;
            c_div.appendChild(p);

            buttons = document.createElement("div");
            buttons.setAttribute("class", "buttons");
            c_div.appendChild(buttons);

            link = document.createElement("a");
            link.setAttribute("href", `${site_characters_url}/${id}`);
            link.innerHTML = "View";
            buttons.appendChild(link);

            dom_character_list.appendChild(c_div);
        }
    } catch (error) {
        const error_message = document.createElement("p");
        error_message.innerHTML = "An error occurred while fetching your list of characters.";
        dom_character_list.appendChild(error_message);
        console.error(error);
        return
    }
}

async function get_character_list() {
    const endpoint = `${base_api_url}/characters`;
    const response = await fetch(endpoint, {
        method: "GET",
        credentials: "same-origin"
    });
    const list = await response.json();
    return list;
}
