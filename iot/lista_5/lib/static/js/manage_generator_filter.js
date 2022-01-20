const sender_form = document.getElementById("sender")
const getter_form = document.getElementById("getter")
const filter_form = document.getElementById("filter")
const button = document.getElementById("button")

const btn = filter_form.getElementsByClassName("btn")[0]

async function add_new(e) {
    e.preventDefault()

    const elem = document.getElementById("path")
    elem.parentElement.append(elem.cloneNode())
}

async function submit_sender(e) {
    e.preventDefault()
    const data = new FormData(e.target);

    const address = data.get("address_s");
    const topic = data.get("path_s");

    const obj = {
        "type": "generator-filter",
        "action": "change_sender",
        "form": {
            "address": address,
            "topic": topic,
        }
    }

    await send_data(obj)

    window.location.reload()
}

async function submit_getter(e) {
    e.preventDefault()
    const data = new FormData(e.target);

    const url = data.get("url")

    const obj = {
        "type": "generator-filter",
        "action": "change_getter",
        "form": {
            "url": url
        }
    }

    await send_data(obj)
    window.location.reload()
}

async function toggle_pause(e) {
    e.preventDefault()

    await send_data({"type": "generator-filter", "action": "toggle_pause", "form": {}})
    window.location.reload()
}

async function submit_filter(e) {
    e.preventDefault()
    const data = new FormData(e.target);

    const paths = [...filter_form.getElementsByClassName("form-control")]
        .map((item) => {return item.value})
        .filter((item) => {return item.length})

    const soft = data.get("soft") == "true" ? true : false

    if(paths.length > 0) {
        const data = {
            "type": "generator-filter",
            "action": "change_filter",
            "form": {
                "soft": soft,
                "paths": paths
            }
        }
        await send_data(data)
        window.location.reload()
    }
}

sender_form.addEventListener("submit", submit_sender)
getter_form.addEventListener("submit", submit_getter)
filter_form.addEventListener("submit", submit_filter)
button.addEventListener("click", toggle_pause)

new_button = document.createElement("button")
new_button.setAttribute("class", "btn btn-outline-success")
new_button.textContent = "Add new"
new_button.addEventListener("click", add_new)
btn.parentElement.appendChild(new_button)