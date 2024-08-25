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
    abilities: {
        strength: {
            score: document.getElementById("abilities.strength.score"),
            modified_score: document.getElementById("abilities.strength.modified_score"),
            modifier: document.getElementById("abilities.strength.modifier")
        },
        dexterity: {
            score: document.getElementById("abilities.dexterity.score"),
            modified_score: document.getElementById("abilities.dexterity.modified_score"),
            modifier: document.getElementById("abilities.dexterity.modifier")
        }
    },
    saves: {
        reflex: {
            value: document.getElementById("saves.reflex.value"),
            modifier: document.getElementById("saves.reflex.modifier")
        }
    },
    update: function(M) {
        let data = M.getData();
        this.abilities.strength.score.value = data.abilities.strength.score;
        this.abilities.strength.modified_score.innerHTML = data.abilities.strength.modified_score;
        this.abilities.strength.modifier.innerHTML = data.abilities.strength.modifier;
        this.abilities.dexterity.score.value = data.abilities.dexterity.score;
        this.abilities.dexterity.modified_score.innerHTML = data.abilities.dexterity.modified_score;
        this.abilities.dexterity.modifier.innerHTML = data.abilities.dexterity.modifier;
        this.saves.reflex.value.value = data.saves.reflex.value;
        this.saves.reflex.modifier.innerHTML = data.saves.reflex.modifier;
    }
}

var C = {
    model: M,
    view: V,
    handler: function() {
        this.view.update(this.model);
    }
}

function initialize_view_listeners(view) {
    view.abilities.strength.score.addEventListener("change", function() {
        let data = M.getData();
        let raw_score = V.abilities.strength.score.value;
        let score = parseInt(raw_score);
        if (isNaN(score)) {
            score = 0;
        }
        data.abilities.strength.score = score;
        M.setData(data);
    });
    view.abilities.dexterity.score.addEventListener("change", function() {
        let data = M.getData();
        let raw_score = V.abilities.dexterity.score.value;
        let score = parseInt(raw_score);
        if (isNaN(score)) {
            score = 0;
        }
        data.abilities.dexterity.score = score;
        M.setData(data);
    });
    view.saves.reflex.value.addEventListener("change", function() {
        let data = M.getData();
        let raw_value = V.saves.reflex.value.value;
        let value = parseInt(raw_value);
        if (isNaN(value)) {
            value = 0;
        }
        data.saves.reflex.value = value;
        M.setData(data);
    });
}

function redirect_to_login() {
    window.location.replace(`${hostname}/login`);
}

window.onload = function() {
    get_character()
        .then((data) => {
            M.data = data;
            initialize_view_listeners(V);
            C.handler.call(C);
        });
}
