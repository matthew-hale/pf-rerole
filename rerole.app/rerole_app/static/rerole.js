"use strict";

var hostname = "http://localhost:5000";
var base_api_url = `${hostname}/api/v0`;

async function get_character() {
    const endpoint = `${base_api_url}/characters/${C_ID}`;
    return fetch(endpoint, {
        method: "GET",
        credentials: "same-origin"
    })
        .then((response) => {
            if (response.status == 401) {
                redirect_to_login();
                return;
            }
            return response.json();
        });
}

async function put_character(d) {
    const endpoint = `${base_api_url}/characters/${C_ID}`;
    return fetch(endpoint, {
        method: "PUT",
        credentials: "same-origin",
        body: JSON.stringify(d),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then((response) => {
            if (response.status == 401) {
                redirect_to_login();
                return;
            }
            return response.json();
        });
}

async function calculate() {
    const endpoint = `${base_api_url}/characters/${C_ID}/calculate`;
    return fetch(endpoint, {
        method: "POST",
        credentials: "same-origin"
    })
        .then((response) => {
            if (response.status == 401) {
                redirect_to_login();
                return;
            }
            return response.json();
        });
}

var M = {
    data: {},
    setData: function(d) {
        this.data = d;
        put_character(this.data)
            .then((response) => {
                if (response.status == 401) {
                    redirect_to_login();
                    return;
                }
                return calculate();
            })
            .then((response) => {
                if (response.status == 401) {
                    redirect_to_login();
                    return;
                }
                return get_character();
            })
            .then((response) => {
                if (response.status == 401) {
                    redirect_to_login();
                    return;
                }
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
    let score;
    let modified_score;
    let modifier;
    let value;

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

    for (const ability of Object.keys(data.abilities)) {
        const abilities = document.getElementById("abilities");
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
    for (const save of Object.keys(data.saves)) {
        const saves = document.getElementById("saves");
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

function redirect_to_login() {
    window.location.replace(`${hostname}/login`);
}

window.onload = function() {
    get_character()
        .then((data) => {
            M.data = data;
            initialize_view(M, V);
            C.handler.call(C);
        });
}
