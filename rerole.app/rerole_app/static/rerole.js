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

class Model {
    constructor(data = {}) {
        this.data = data;
    }
    setData(data) {
        this.data = data;
        return put_character(this.data)
            .then((response) => {
                this.data = response;
                return response;
            });
    }
    getData() {
        return this.data;
    }
}

class Sheet {
    constructor(model) {
        const data = model.getData();

        this.model = model;

        this.modal = document.getElementById("modal");

        this.view = {};
        this.view.abilities = {};
        this.view.saves = {};
        this.view.feats = {};

        this.document = {};
        this.document.general = document.getElementById("general");
        this.document.abilities = document.getElementById("abilities");
        this.document.saves = document.getElementById("saves");
        this.document.feats = document.getElementById("feats");

        this.view.name = document.createElement("input");
        this.view.name.setAttribute("type", "text");
        let name_span = document.createElement("span");
        name_span.innerHTML = "Name:";
        let name_label = document.createElement("label");
        name_label.append(name_span, this.view.name);
        this.document.general.append(name_label);

        for (const ability of Object.keys(data.abilities)) {
            const this_ability = data.abilities[ability];
            this.view.abilities[ability] = {};
            let ability_div = document.createElement("div");
            ability_div.classList.add("ability");
            this.document.abilities.append(ability_div);

            const ability_score = document.createElement("input");
            this.view.abilities[ability].score = ability_score;
            ability_score.setAttribute("type", "text");
            let ability_label_span = document.createElement("span");
            ability_label_span.innerHTML = ability;
            let ability_label = document.createElement("label");
            ability_label.append(ability_label_span, ability_score);

            this.view.abilities[ability].modified_score = document.createElement("p");
            let ability_modified_score_span = document.createElement("span");
            ability_modified_score_span.innerHTML = "Modified score:";
            let ability_modified_score_label = document.createElement("label");
            ability_modified_score_label.append(ability_modified_score_span, this.view.abilities[ability].modified_score);


            this.view.abilities[ability].modifier = document.createElement("p");
            let ability_modifier_span = document.createElement("span");
            ability_modifier_span.innerHTML = "Modifier:";
            let ability_modifier_label = document.createElement("label");
            ability_modifier_label.append(ability_modifier_span, this.view.abilities[ability].modifier);

            this.view.abilities[ability].get = function() {
                let ability_score = parseInt(this.score.value);
                if (isNaN(ability_score)) {
                    ability_score = 0;
                }
                return {
                    score: ability_score
                }
            }

            this.view.abilities[ability].set = function(data) {
                this.score.value = data.score.toString() || "0";
                this.modified_score.innerHTML = data.modified_score.toString() || "0";
                this.modifier.innerHTML = data.modifier.toString() || "0";
            };

            ability_score.addEventListener("change", function(ability) {
                const data = this.model.getData();
                const view_ability = this.view.abilities[ability].get();
                const old_ability = data.abilities[ability];
                const new_ability = {...old_ability, ...view_ability};
                data.abilities[ability] = new_ability;
                this.model.setData(data)
                    .then(() => {
                        this.updateView();
                    });
            }.bind(this, ability));

            ability_div.append(
                ability_label,
                ability_modified_score_label,
                ability_modifier_label,
            );
        }

        for (const save of Object.keys(data.saves)) {
            const this_save = data.saves[save];
            this.view.saves[save] = {};
            const save_div = document.createElement("div");
            save_div.classList.add("save");
            this.document.saves.append(save_div);

            const save_value = document.createElement("input");
            this.view.saves[save].value = save_value;
            save_value.setAttribute("type", "text");
            const save_label_span = document.createElement("span");
            save_label_span.innerHTML = save;
            const save_label = document.createElement("label");
            save_label.append(save_label_span, save_value);

            const save_modifier = document.createElement("p");
            this.view.saves[save].modifier = save_modifier;
            save_modifier.innerHTML = this_save.modifier.toString() || "0";
            const save_modifier_label_span = document.createElement("span");
            save_modifier_label_span.innerHTML = "Modifier:";
            const save_modifier_label = document.createElement("label");
            save_modifier_label.append(save_modifier_label_span, save_modifier);

            this.view.saves[save].get = function() {
                let save_value = parseInt(this.value.value);
                if (isNaN(save_value)) {
                    save_value = 0;
                }
                return {
                    value: save_value
                }
            };

            this.view.saves[save].set = function(data) {
                this.value.value = data.value.toString() || "0";
                this.modifier.innerHTML = data.modifier.toString() || "0";
            };

            save_value.addEventListener("change", function(save) {
                const data = this.model.getData();
                const view_save = this.view.saves[save].get();
                const old_save = data.saves[save];
                const new_save = {...old_save, ...view_save};
                data.saves[save] = new_save;
                this.model.setData(data)
                    .then(() => {
                        this.updateView();
                    });
            }.bind(this, save));

            save_div.append(save_label, save_modifier_label);
        }

        for (const feat of Object.keys(data.feats)) {
            const this_feat = data.feats[feat];

            this.view.feats[feat] = {};

            const feat_button = document.createElement("button");
            feat_button.setAttribute("type", "button");
            feat_button.innerHTML = feat;
            this.view.feats[feat].button = feat_button;

            this.document.feats.append(this.view.feats[feat].button);
        }

        this.updateView();
    }
    updateView() {
        const data = this.model.getData();
        this.view.name.value = data.name || "Unnamed";

        for (const ability of Object.keys(data.abilities)) {
            this.view.abilities[ability].set(data.abilities[ability]);
        }

        for (const save of Object.keys(data.saves)) {
            this.view.saves[save].set(data.saves[save]);
        }
    }
    editFeat(name) {
        this.EditFeat = new EditFeat(name, this.model.getData());
        this.modal.appendChild(this.EditFeat.root);

        this.EditFeat.cancel_button.addEventListener("click", function() {
            this.EditFeat.close();
        }.bind(this));
        this.EditFeat.ok_button.addEventListener("click", function() {
            const original_feat_name = this.EditFeat.original_name;
            const feat_name = this.EditFeat.getName();
            const feat_data = this.EditFeat.getFeat();

            const is_new_feat = (original_feat_name === "");
            const is_new_feat_name = (feat_name !== original_feat_name);

            if (is_new_feat) {
                this.newFeat(feat_name, feat_data);
                this.EditFeat.close();
                return;
            }
            if (!is_new_feat && is_new_feat_name) {
                this.newFeat(feat_name, feat_data)
                    .then(() => {
                        this.deleteFeat(original_feat_name);
                    })
                    .finally(() => {
                        this.EditFeat.close();
                    });
                return;
            }
            this.updateFeat(feat_name, feat_data);
            this.EditFeat.close();
        }.bind(this));
        this.EditFeat.delete_button.addEventListener("click", function() {
            const feat_name = this.EditFeat.getName();
            this.deleteFeat(feat_name);
            this.EditFeat.close();
        }.bind(this));
        this.EditFeat.close = function() {
            this.closeModal();
            this.EditFeat.root.outerHTML = "";
            this.EditFeat = null;
        }.bind(this);

        this.openModal();
    }
    newFeat(name, feat_data) {
        const data = this.model.getData();
        this.view.feats[name] = {};

        const feat_button = document.createElement("button");
        feat_button.setAttribute("type", "button");
        feat_button.innerHTML = name;
        this.view.feats[name].button = feat_button;

        this.document.feats.append(feat_button);

        data.feats[name] = feat_data;

        return this.model.setData(data)
            .then(() => {
                this.updateView();
            });
    }
    updateFeat(name, feat_data) {
        const data = this.model.getData();
        const current_feat = data.feats[name] || {};
        const new_feat = {...current_feat, ...feat_data};
        data.feats[name] = new_feat;

        return this.model.setData(data)
            .then(() => {
                this.updateView();
            });
    }
    deleteFeat(name) {
        const data = this.model.getData();
        delete data.feats[name];
        this.view.feats[name].button.outerHTML = "";
        delete this.view.feats[name];

        return this.model.setData(data)
            .then(() => {
                this.updateView();
            });
    }
    closeModal() {
        this.modal.style.display = "none";
    }
    openModal() {
        this.modal.style.display = "flex";
    }
}

class EditFeat{
    constructor(name, sheet = {}) {
        this.root = document.createElement("div");
        this.root.classList.add("edit-modal");
        this.root.classList.add("feat");

        this.original_name = name;

        const data = sheet.feats[name] || {};

        this.name_label = document.createElement("label");
        let span = document.createElement("span");
        span.innerHTML = "Name:";
        this.name = document.createElement("input");
        this.name.setAttribute("type", "text");
        this.name.value = name;
        this.name_label.append(span, this.name);

        this.description_label = document.createElement("label");
        this.description_label.setAttribute("name", "description");

        span = document.createElement("span");
        span.innerHTML = "Description:";
        this.description = document.createElement("textarea");
        let description = data.description || "";
        this.description.value = description;
        this.description_label.append(span, this.description);

        this.type_label = document.createElement("label");
        this.type_label.setAttribute("name", "type");

        span = document.createElement("span");
        span.innerHTML = "Type:";
        this.type = document.createElement("input");
        this.type.setAttribute("type", "text");
        let type = data.type || "";
        this.type.value = type;
        this.type_label.append(span, this.type);

        this.effect_objs = [];
        this.effects = document.createElement("label");
        span = document.createElement("span");
        span.innerHTML = "Effects:";
        let div = document.createElement("div");
        div.classList.add("effects");
        this.effects.append(span, div);

        const effects = data.effects || [];
        for (const effect of effects) {
            let e = new Effect(sheet, effect);
            this.effect_objs.push(e);
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
        delete_button.classList.add("delete");
        delete_button.innerHTML = "Delete";
        right_div.append(ok_button, delete_button);

        this.cancel_button = cancel_button;
        this.ok_button = ok_button;
        this.delete_button = delete_button;

        this.buttons.append(left_div, right_div);

        this.root.append(
            this.name_label,
            this.description_label,
            this.type_label,
            this.effects,
            this.buttons,
        );
    }
    getName() {
        return this.name.value;
    }
    getFeat() {
        let feat = {};
        feat["description"] = this.description.value;
        feat["type"] = this.type.value;
        let effects = [];
        for (const effect of this.effect_objs) {
            effects.push(effect.getEffect());
        }
        if (effects) {
            feat["effects"] = effects;
        }

        return feat;
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

var SHEET;
window.onload = function() {
    get_character()
        .then((data) => {
            const model = new Model(data);
            SHEET = new Sheet(model);
        });
}
