const sender_form = document.getElementById("sender")
const getter_form = document.getElementById("getter")
const button = document.getElementById("button")

async function submit_sender(e) {
    e.preventDefault()
    const data = new FormData(e.target);

    const address = data.get("address_s");
    const topic = data.get("path_s");

    const obj = {
        "type": "generator",
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
    const path = data.get("path_g")
    const is_json = document.getElementById("json").checked
    const type = data.get("type")

    const obj = {
        "type": "generator",
        "action": "change_getter",
        "form": {
            "url": url,
            "path": path,
            "json": is_json,
            "type": type
        }
    }

    await send_data(obj)
    window.location.reload()
}

async function toggle_pause(e) {
    e.preventDefault()

    await send_data({"type": "generator", "action": "toggle_pause", "form": {}})
    window.location.reload()
}


sender_form.addEventListener("submit", submit_sender)
getter_form.addEventListener("submit", submit_getter)
button.addEventListener("click", toggle_pause)
