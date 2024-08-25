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
    name: document.getElementById("name"),
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

    view.name.addEventListener("change", function() {
        let data = model.getData();
        let name = view.name.value;
        data.name = name;
        model.setData(data);
    })

    for (const ability of Object.keys(data.abilities)) {
        view.abilities[ability] = {
            score: document.getElementById(`abilities.${ability}.score`),
            modified_score: document.getElementById(`abilities.${ability}.modified_score`),
            modifier: document.getElementById(`abilities.${ability}.modifier`)
        }
        view.abilities[ability].score.addEventListener("change", function() {
            update_model_ability(model, view, ability);
        });
    }
    for (const save of Object.keys(data.saves)) {
        view.saves[save] = {
            value: document.getElementById(`saves.${save}.value`),
            modifier: document.getElementById(`saves.${save}.modifier`)
        }
        view.saves[save].value.addEventListener("change", function() {
            update_model_save(model, view, save);
        });
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
