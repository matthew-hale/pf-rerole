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
        },
        constitution: {
            score: document.getElementById("abilities.constitution.score"),
            modified_score: document.getElementById("abilities.constitution.modified_score"),
            modifier: document.getElementById("abilities.constitution.modifier")
        },
        intelligence: {
            score: document.getElementById("abilities.intelligence.score"),
            modified_score: document.getElementById("abilities.intelligence.modified_score"),
            modifier: document.getElementById("abilities.intelligence.modifier")
        },
        wisdom: {
            score: document.getElementById("abilities.wisdom.score"),
            modified_score: document.getElementById("abilities.wisdom.modified_score"),
            modifier: document.getElementById("abilities.wisdom.modifier")
        },
        charisma: {
            score: document.getElementById("abilities.charisma.score"),
            modified_score: document.getElementById("abilities.charisma.modified_score"),
            modifier: document.getElementById("abilities.charisma.modifier")
        },
    },
    saves: {
        fortitude: {
            value: document.getElementById("saves.fortitude.value"),
            modifier: document.getElementById("saves.fortitude.modifier")
        },
        reflex: {
            value: document.getElementById("saves.reflex.value"),
            modifier: document.getElementById("saves.reflex.modifier")
        },
        will: {
            value: document.getElementById("saves.will.value"),
            modifier: document.getElementById("saves.will.modifier")
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
        this.abilities.constitution.score.value = data.abilities.constitution.score;
        this.abilities.constitution.modified_score.innerHTML = data.abilities.constitution.modified_score;
        this.abilities.constitution.modifier.innerHTML = data.abilities.constitution.modifier;
        this.abilities.intelligence.score.value = data.abilities.intelligence.score;
        this.abilities.intelligence.modified_score.innerHTML = data.abilities.intelligence.modified_score;
        this.abilities.intelligence.modifier.innerHTML = data.abilities.intelligence.modifier;
        this.abilities.wisdom.score.value = data.abilities.wisdom.score;
        this.abilities.wisdom.modified_score.innerHTML = data.abilities.wisdom.modified_score;
        this.abilities.wisdom.modifier.innerHTML = data.abilities.wisdom.modifier;
        this.abilities.charisma.score.value = data.abilities.charisma.score;
        this.abilities.charisma.modified_score.innerHTML = data.abilities.charisma.modified_score;
        this.abilities.charisma.modifier.innerHTML = data.abilities.charisma.modifier;

        this.saves.fortitude.value.value = data.saves.fortitude.value;
        this.saves.fortitude.modifier.innerHTML = data.saves.fortitude.modifier;
        this.saves.reflex.value.value = data.saves.reflex.value;
        this.saves.reflex.modifier.innerHTML = data.saves.reflex.modifier;
        this.saves.will.value.value = data.saves.will.value;
        this.saves.will.modifier.innerHTML = data.saves.will.modifier;
    }
}

var C = {
    model: M,
    view: V,
    handler: function() {
        this.view.update(this.model);
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

function initialize_view_listeners(model, view) {
    view.abilities.strength.score.addEventListener("change", function() {
        update_model_ability(model, view, "strength");
    });
    view.abilities.dexterity.score.addEventListener("change", function() {
        update_model_ability(model, view, "dexterity");
    });
    view.abilities.constitution.score.addEventListener("change", function() {
        update_model_ability(model, view, "constitution");
    });
    view.abilities.intelligence.score.addEventListener("change", function() {
        update_model_ability(model, view, "intelligence");
    });
    view.abilities.wisdom.score.addEventListener("change", function() {
        update_model_ability(model, view, "wisdom");
    });
    view.abilities.charisma.score.addEventListener("change", function() {
        update_model_ability(model, view, "charisma");
    });
    view.saves.fortitude.value.addEventListener("change", function() {
        update_model_save(model, view, "fortitude");
    });
    view.saves.reflex.value.addEventListener("change", function() {
        update_model_save(model, view, "reflex");
    });
    view.saves.will.value.addEventListener("change", function() {
        update_model_save(model, view, "will");
    });
}

function redirect_to_login() {
    window.location.replace(`${hostname}/login`);
}

window.onload = function() {
    initialize_view_listeners(M, V);
    get_character()
        .then((data) => {
            M.data = data;
            C.handler.call(C);
        });
}
