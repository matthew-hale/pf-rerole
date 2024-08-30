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


class EditFeat{
    constructor(name, sheet = {}, data = {}) {
        this.root = document.createElement("div");
        this.root.classList.add("edit-modal");
        this.root.classList.add("feat");

        this.title = document.createElement("h3");
        this.title.innerHTML = name;

        this.description = document.createElement("label");
        this.description.setAttribute("name", "description");

        let span = document.createElement("span");
        span.innerHTML = "Description:";
        let input = document.createElement("textarea");
        input.value = data.description;
        this.description.append(span, input);

        this.type = document.createElement("label");
        this.type.setAttribute("name", "type");

        span = document.createElement("span");
        span.innerHTML = "Type:";
        input = document.createElement("input");
        input.setAttribute("type", "text");
        this.type.append(span, input);

        this.effects = document.createElement("label");
        span = document.createElement("span");
        span.innerHTML = "Effects:";
        let div = document.createElement("div");
        div.classList.add("effects");
        this.effects.append(span, div);

        const effects = data.effects || [];
        for (const effect of effects) {
            let e = new Effect(sheet, effect);
            div.appendChild(e.root);
        }

        this.buttons = document.createElement("div");
        this.buttons.classList.add("buttons");
        let left_div = document.createElement("div");
        let right_div = document.createElement("div");

        let cancel_button = document.createElement("button");
        cancel_button.setAttribute("type", "button");
        cancel_button.innerHTML = "Cancel";
        left_div.append(cancel_button);

        let ok_button = document.createElement("button");
        ok_button.setAttribute("type", "button");
        ok_button.innerHTML = "Ok";
        let delete_button = document.createElement("button");
        delete_button.setAttribute("type", "button");
        delete_button.innerHTML = "Delete";
        right_div.append(ok_button, delete_button);

        this.buttons.append(left_div, right_div);

        this.root.append(
            this.title,
            this.description,
            this.type,
            this.effects,
            this.buttons,
        );
    }
}

class Effect {
    static none = "(None)";
    static all = "--ALL--";

    constructor(sheet = {}, effect_data = {}) {
        this.root = document.createElement("div");
        this.root.classList.add("effect");

        this.value = document.createElement("input");
        this.type = document.createElement("select");
        this.magic = document.createElement("label");
        this.group = document.createElement("div");

        this.value.setAttribute("type", "text");
        let value = effect_data.value || 0;
        this.value.setAttribute("value", `${value}`);

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
        let type = effect_data.type || Effect.none;
        if (!type in EFFECT_TYPES) {
            type = Effect.none;
        }
        this.type.value = type;

        let magic_checkbox = document.createElement("input");
        magic_checkbox.setAttribute("type", "checkbox");
        let magic_state = effect_data.magic || false;
        magic_checkbox.checked = magic_state;
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

        const affects = effect_data.affects || {};
        const selected_groups = Object.keys(affects);
        for (const group of ["abilities", "saves", "skills"]) {
            const group_items = Object.keys(sheet[group]);
            const group_is_selected = selected_groups.includes(group);
            let selected_items = [];
            if (group_is_selected) {
                let value = affects[group];
                if (typeof value === 'string' || value instanceof String) {
                    selected_items = [value];
                }
                if (Array.isArray(value)) {
                    selected_items = value;
                }
            }
            const affects_obj = new Affects(group, group_items, group_is_selected, selected_items);
            this.group.append(affects_obj.label, affects_obj.menu);
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
}

class Affects {
    constructor(group, items, group_selected = false, items_selected = []) {
        this.groupName = group;

        this.label = document.createElement("label");
        this.label.classList.add("affects-group");

        this.input = document.createElement("input");
        this.input.setAttribute("type", "checkbox");
        this.input.setAttribute("value", group);
        this.input.checked = group_selected;
        this.label.append(this.input);

        this.input.addEventListener("change", this.toggleMenu.bind(this));

        let span = document.createElement("span");
        span.innerHTML = group;
        this.label.append(span);

        this.menu_obj = new NamesMenu(items, items_selected);
        this.menu = this.menu_obj.root;

        this.toggleMenu();
    }
    toggleMenu() {
        const state = this.label.querySelector("input").checked;
        if (state) {
            this.menu.style.display = "block";
        } else {
            this.menu.style.display = "none";
            this.menu_obj.toggleDisplay("", true);
        }
    }
    getValue() {
        const group_name = this.groupName;
        const is_selected = this.input.checked;
        if (!is_selected) {
            return {};
        }
        let output = {};
        output[group_name] = this.menu_obj.getSelectedValue()
        return output;
    }
}

class NamesMenu {
    static all = "--ALL--";
    constructor(items, selected = []) {
        this.root = document.createElement("div");
        this.root.classList.add("affects-names-menu");

        this.selected = document.createElement("div");
        this.selected.classList.add("affects-names-selected");
        let span = document.createElement("span");
        span.innerHTML = NamesMenu.all;
        this.selected.appendChild(span);

        this.selected.addEventListener("click", this.toggleDisplay.bind(this));

        this.dropdown = document.createElement("div");
        this.dropdown.classList.add("affects-names-dropdown");

        for (const item of items) {
            let label = document.createElement("label");
            label.setAttribute("name", item);
            let input = document.createElement("input");
            input.setAttribute("type", "checkbox");
            input.setAttribute("value", item);
            input.checked = false;
            if (selected.includes(item)) {
                input.checked = true;
            }
            let span = document.createElement("span");
            span.innerHTML = item;

            input.addEventListener("change", this.setValue.bind(this));

            label.append(input, span);
            this.dropdown.appendChild(label);
        }

        this.setValue("");

        this.root.append(this.selected, this.dropdown);
    }
    setValue(evt) {
        const all_inputs = Array.from(this.dropdown.querySelectorAll("input"));
        const selected_inputs = all_inputs
            .filter((input) => input.checked);

        if (selected_inputs.length == 0) {
            this.selected.firstElementChild.innerHTML = NamesMenu.all;
            return
        }
        const one_selected = selected_inputs.length == 1;
        const multiple_selected = selected_inputs.length > 1;
        const all_selected = selected_inputs.length == all_inputs.length;

        let output_string;
        if (one_selected) {
            output_string = selected_inputs[0].value;
        }
        if (multiple_selected) {
            output_string = "(multiple selected)";
        }
        if (all_selected) {
            output_string = Effect.all;
        }

        this.selected.firstElementChild.innerHTML = output_string;
    }
    getSelectedValue() {
        const all_inputs = Array.from(this.dropdown.querySelectorAll("input"));
        const selected = all_inputs
            .filter((input) => input.checked)
            .map((input) => input.value);

        if (selected.length == 0 || selected.length == all_inputs.length) {
            return true;
        }
        if (selected.length == 1) {
            return selected[0];
        }
        return selected;
    }
    toggleDisplay(evt, hide = false) {
        if (hide) {
            this.dropdown.style.display = "none";
            return
        }
        let current_display = this.dropdown.style.display;
        if (current_display === "none" || current_display === "") {
            this.dropdown.style.display = "flex";
        } else {
            this.dropdown.style.display = "none";
        }
    }
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

window.onload = function() {
    get_character()
        .then((data) => {
            M.data = data;
            initialize_view(M, V);
            C.handler.call(C);
        });
}
