"use strict";

var hostname = "http://localhost:5000";
var base_api_url = `${hostname}/api/v0`;

var EFFECT_TYPES = [
    "untyped",
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
            logout();
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
            logout();
        });
}

async function calculate() {
    const endpoint = `${base_api_url}/characters/${C_ID}/calculate`;
    return fetch(endpoint, {
        method: "POST",
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
            logout();
        });
}

var M = {
    data: {},
    setData: function(d) {
        this.data = d;
        put_character(this.data)
            .then((response) => {
                return calculate();
            })
            .then((response) => {
                return get_character();
            })
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
    let type;
    let affects;
    let option;

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

    const feats = document.getElementById("feats");
    for (const feat of Object.keys(data.feats)) {
        const feat_data = data.feats[feat];
        const feat_keys = Object.keys(feat_data);

        let f = document.createElement("details");
        f.setAttribute("class", "feat");
        feats.appendChild(f);

        summary = document.createElement("summary");
        summary.innerHTML = feat;
        f.appendChild(summary);

        label = document.createElement("label");
        label.setAttribute("for", `feats.${feat}.description`)
        label.innerHTML = "Description";
        f.appendChild(label);

        description = document.createElement("textarea");
        description.setAttribute("id", `feats.${feat}.description`);
        description.addEventListener("change", function() {
            update_model_feat(model, view, feat);
        });
        f.appendChild(description);

        label = document.createElement("label");
        label.setAttribute("for", `feats.${feat}.value`)
        label.innerHTML = "Value";
        f.appendChild(label);

        value = document.createElement("input");
        value.setAttribute("id", `feats.${feat}.value`)
        value.setAttribute("type", "text")
        value.addEventListener("change", function() {
            update_model_feat(model, view, feat);
        });
        f.appendChild(value);

        type = document.createElement("select");
        type.setAttribute("id", `feats.${feat}.type`);
        for (const t of EFFECT_TYPES) {
            option = document.createElement("option");
            option.setAttribute("value", t);
            option.innerHTML = t;
            type.appendChild(option);
        }
        type.addEventListener("change", function() {
            update_model_feat(model, view, feat);
        });
        f.appendChild(type);

        view.feats[feat] = {
            description: description,
            value: value,
            type: type,
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

        for (const feat of Object.keys(this.feats)) {
            this.feats[feat].description.value = data.feats[feat].description;
            this.feats[feat].value.value = data.feats[feat].value;
            this.feats[feat].type.value = data.feats[feat].type;
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

function update_model_feat(m, v, feat_name) {
    let data = m.getData();
    let feat = data.feats[feat_name];
    feat.description = v.feats[feat_name].description.value;
    let raw_value = v.feats[feat_name].value.value;
    let value = parseInt(raw_value);
    if (isNaN(value)) {
        value = 0;
    }
    feat.value = value;
    feat.type = v.feats[feat_name].type.value;
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
