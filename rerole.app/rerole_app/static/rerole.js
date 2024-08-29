"use strict";

var hostname = "http://localhost:5000";
var base_api_url = `${hostname}/api/v0`;

var EFFECT_TYPES = [
    "alchemical",
    "armor",
    "bab",
    "circumstance",
    "competence",
    "deflection",
    "dodge",
    "enhancement",
    "inherent",
    "insight",
    "luck",
    "morale",
    "natural armor",
    "profane",
    "racial",
    "resistance",
    "sacred",
    "shield",
    "size",
    "trait",
];


class Effect {
    static none = "(None)";
    static all = "--ALL--";

    constructor() {
        this.root = document.createElement("div");
        this.root.classList.add("effect");

        this.value = document.createElement("input");
        this.type = document.createElement("select");
        this.magic = document.createElement("label");
        this.group = document.createElement("div");

        this.value.setAttribute("type", "text");
        this.value.setAttribute("value", "0");

        let magic_checkbox = document.createElement("input");
        magic_checkbox.setAttribute("type", "checkbox");
        this.magic.append(magic_checkbox, "magic");

        this.group.classList.add("affects-groups");

        let div;

        div = document.createElement("div");
        this.root.appendChild(div);
        div.appendChild(this.value);

        div = document.createElement("div");
        this.root.appendChild(div);
        div.appendChild(this.type);

        div = document.createElement("div");
        this.root.appendChild(div);
        div.appendChild(this.magic);

        div = document.createElement("div");
        this.root.appendChild(div);
        div.appendChild(this.group);

        let option = document.createElement("option");
        option.setAttribute("value", Effect.none);
        option.innerHTML = Effect.none;
        this.type.appendChild(option);
        for (const t of EFFECT_TYPES) {
            let option = document.createElement("option");
            option.setAttribute("value", t);
            option.innerHTML = t;
            this.type.appendChild(option);
        }
    }
    initGroups(groups, sheet) {
        this.resetGroups();
        for (const group of groups) {
            let label = document.createElement("label");
            label.setAttribute("name", group);
            label.classList.add("affects-group");
            this.group.appendChild(label);

            let check = document.createElement("input");
            check.setAttribute("type", "checkbox");
            check.setAttribute("value", group);
            check.setAttribute("onchange", "toggleMenu(this)");
            label.appendChild(check);
            label.append(group);

            let names_menu = document.createElement("div");
            names_menu.classList.add("affects-names-menu");
            this.group.append(names_menu);

            let selected = document.createElement("div");
            selected.setAttribute("onclick", "toggleDropdown(this)");
            selected.classList.add("affects-names-selected");
            names_menu.appendChild(selected);

            let selection = document.createElement("p");
            selection.innerHTML = Effect.all;
            selected.appendChild(selection);

            let dropdown = document.createElement("div");
            dropdown.classList.add("affects-names-dropdown");
            names_menu.appendChild(dropdown);

            let items = Object.keys(sheet[group]);
            for (const item of items) {
                let label = document.createElement("label");
                label.setAttribute("name", item);

                let check = document.createElement("input");
                check.setAttribute("type", "checkbox");
                check.setAttribute("value", item);
                check.setAttribute("onchange", "checkboxChanged(this)");
                label.append(check, item);

                dropdown.appendChild(label);
            }
        }
    }
    getEffect() {
        let effect = {};

        let value = parseInt(this.value.value);
        if (isNaN(value)) {
            value = 0;
        }
        effect["value"] = value;

        let type = this.type.value;
        if (type !== Effect.none) {
            effect["type"] = type;
        }
        let magic = this.magic.firstElementChild.checked;
        if (magic) {
            effect["magic"] = true;
        }

        let affects = {};
        Array.from(this.group.querySelectorAll(".affects-group"))
            .map((label) => label.firstChild)
            .filter((input) => input.checked)
            .forEach((input) => {
                const group = input.value;
                affects[group] = true;

                const menu = input.parentElement.nextElementSibling;
                const all_options = Array.from(menu.querySelectorAll("input"));
                let selected_values = all_options
                    .filter((input) => input.checked)
                    .map((input) => input.value);

                const none_selected = selected_values.length == 0;
                const one_selected = selected_values.length == 1;
                const all_selected = selected_values.length == all_options.length;
                if (none_selected || all_selected) {
                    return
                }
                if (one_selected) {
                    selected_values = selected_values[0];
                }
                affects[group] = selected_values;
            });
        if (Object.keys(affects).length !== 0) {
            effect["affects"] = affects;
        }

        return effect;
    }
    resetGroups() {
        this.group.innerHTML = "";
    }
}

function toggleMenu(obj) {
    const state = obj.checked;
    const menu = obj.parentElement.nextElementSibling;
    if (state) {
        menu.style.display = "block";
    } else {
        menu.style.display = "none";
        const selected = menu.querySelector(".affects-names-selected");
        toggleDropdown(selected, true);
    }
}

function toggleDropdown(obj, hide = false) {
    const parent = obj.parentElement;
    const dropdown = parent.querySelector(".affects-names-dropdown");
    if (hide) {
        dropdown.style.display = "none";
        return
    }
    let current_display = dropdown.style.display;
    if (current_display === "none" || current_display === "") {
        dropdown.style.display = "flex";
    } else {
        dropdown.style.display = "none";
    }
}

function checkboxChanged(obj) {
    //TODO: this is all obviously janky
    const dropdown = obj.parentElement.parentElement;
    const top_menu = dropdown.parentElement;
    const output = top_menu.querySelector(".affects-names-selected").firstChild;

    const all_inputs = Array.from(dropdown.querySelectorAll("input"));
    let selected_inputs = all_inputs
        .filter((input) => input.checked)
        .map((input) => input.value);

    if (selected_inputs.length == 0) {
        output.innerHTML = Effect.all;
        return
    }
    const one_selected = selected_inputs.length == 1;
    const multiple_selected = selected_inputs.length > 1;
    const all_selected = selected_inputs.length == all_inputs.length;

    let output_string;
    if (one_selected) {
        output_string = selected_inputs[0];
    }
    if (multiple_selected) {
        output_string = "(multiple selected)";
    }
    if (all_selected) {
        output_string = Effect.all;
    }

    output.innerHTML = output_string;
}


async function get_character() {
    const endpoint = `${base_api_url}/characters/${C_ID}`;
    return fetch(endpoint, {
        method: "GET",
        headers: {
            Authorization: get_authorization_header(),
        },
        credentials: "same-origin",
    })
        .then((response) => {
            if (response.status == 401) {
                throw "401";
            }
            return response.json();
        })
        .catch((err) => {
            if (err == "401") {
                logout();
            }
            console.log(err);
        });
}

async function put_character(d) {
    const endpoint = `${base_api_url}/characters/${C_ID}`;
    return fetch(endpoint, {
        method: "PUT",
        credentials: "same-origin",
        body: JSON.stringify(d),
        headers: {
            "Content-Type": "application/json",
            Authorization: get_authorization_header(),
        },
    })
        .then((response) => {
            if (response.status == 401) {
                throw "401";
            }
            return response.json();
        })
        .catch((err) => {
            if (err == "401") {
                logout();
            }
            console.log(err);
        });
}


var M = {
    data: {},
    setData: function(d) {
        this.data = d;
        put_character(this.data)
            .then((response) => {
                this.data = response;
                C.handler.call(C);
            });
    },
    getData: function() {
        return this.data;
    }
}

var V = {
    abilities: {},
    saves: {},
    feats: {},
}

var C = {
    model: M,
    view: V,
    handler: function() {
        this.view.update(this.model);
    }
}

function initialize_view(model, view) {
    const data = model.getData();

    let label;
    let summary;
    let score;
    let modified_score;
    let modifier;
    let value;
    let description;

    const general = document.getElementById("general");
    label = document.createElement("label");
    label.setAttribute("for", "name");
    label.innerHTML = "Name:";
    general.appendChild(label);

    view.name = document.createElement("input");
    view.name.setAttribute("id", "name");
    view.name.setAttribute("type", "text");
    view.name.addEventListener("change", function() {
        let data = model.getData();
        let name = view.name.value;
        data.name = name;
        model.setData(data);
    })
    general.appendChild(view.name);

    const abilities = document.getElementById("abilities");
    for (const ability of Object.keys(data.abilities)) {
        let a = document.createElement("div");
        a.setAttribute("class", "ability");
        abilities.appendChild(a);

        label = document.createElement("label");
        label.setAttribute("for", `abilities.${ability}.score`);
        label.innerHTML = ability;
        a.appendChild(label);

        score = document.createElement("input");
        score.setAttribute("id", `abilities.${ability}.score`);
        score.setAttribute("type", "text");
        score.addEventListener("change", function() {
            update_model_ability(model, view, ability);
        });
        a.appendChild(score);

        label = document.createElement("label");
        label.setAttribute("for", `abilities.${ability}.modified_score`);
        label.innerHTML = "Modified score:";
        a.appendChild(label);

        modified_score = document.createElement("p");
        modified_score.setAttribute("id", `abilities.${ability}.modified_score`);
        a.appendChild(modified_score);

        label = document.createElement("label");
        label.setAttribute("for", `abilities.${ability}.modifier`);
        label.innerHTML = "Modifier:";
        a.appendChild(label);

        modifier = document.createElement("p");
        modifier.setAttribute("id", `abilities.${ability}.modifier`);
        a.appendChild(modifier);

        view.abilities[ability] = {
            score: score,
            modified_score: modified_score,
            modifier: modifier
        }
    }

    const saves = document.getElementById("saves");
    for (const save of Object.keys(data.saves)) {
        let s = document.createElement("div");
        s.setAttribute("class", "save");
        saves.appendChild(s);

        label = document.createElement("label");
        label.setAttribute("for", `saves.${save}.value`);
        label.innerHTML = save;
        s.appendChild(label);

        value = document.createElement("input");
        value.setAttribute("id", `saves.${save}.value`);
        value.setAttribute("type", "text");
        value.addEventListener("change", function() {
            update_model_save(model, view, save);
        });
        s.appendChild(value);

        label = document.createElement("label");
        label.setAttribute("for", `saves.${save}.modifier`);
        label.innerHTML = "Modifier:";
        s.appendChild(label);

        modifier = document.createElement("p");
        modifier.setAttribute("id", `saves.${save}.modifier`);
        s.appendChild(modifier);

        view.saves[save] = {
            value: value,
            modifier: modifier
        }
    }

    view.update = function(model) {
        let data = model.getData();

        this.name.value = data.name;

        for (const ability of Object.keys(this.abilities)) {
            this.abilities[ability].score.value = data.abilities[ability].score;
            this.abilities[ability].modified_score.innerHTML = data.abilities[ability].modified_score;
            this.abilities[ability].modifier.innerHTML = data.abilities[ability].modifier;
        }

        for (const save of Object.keys(this.saves)) {
            this.saves[save].value.value = data.saves[save].value;
            this.saves[save].modifier.innerHTML = data.saves[save].modifier;
        }
    }
}

function update_model_ability(m, v, ability_name) {
    let data = m.getData();
    let raw_score = v.abilities[ability_name].score.value;
    let score = parseInt(raw_score);
    if (isNaN(score)) {
        score = 0;
    }
    data.abilities[ability_name].score = score;
    m.setData(data);
}

function update_model_save(m, v, save_name) {
    let data = m.getData();
    let raw_value = v.saves[save_name].value.value;
    let value = parseInt(raw_value);
    if (isNaN(value)) {
        value = 0;
    }
    data.saves[save_name].value = value;
    m.setData(data);
}

function logout() {
    console.log("logout");
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

function produce_effect() {
    let effect = E.getEffect();
    let output = document.getElementById("test-output");
    output.innerHTML = JSON.stringify(effect);
}

var E = new Effect();

window.onload = function() {
    get_character()
        .then((data) => {
            M.data = data;
            initialize_view(M, V);
            C.handler.call(C);

            E.initGroups(["abilities", "saves", "skills"], data);

            let effect_entry_root = document.getElementById("test");
            effect_entry_root.appendChild(E.root);
        });
}
