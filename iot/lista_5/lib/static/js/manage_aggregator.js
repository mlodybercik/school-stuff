const change_form = document.getElementById("change")
const add_form = document.getElementById("add")
const remove_form = document.getElementById("remove")

//* both add and change are almost exactly the same, i should change the form generation
//* to allow same name accross different forms. that would allow me to write single function here.
// TODO: improve form generation to allow same names accros different forms


async function submit_add(e) {
    e.preventDefault()

    const data = new FormData(e.target)

    const name = data.get("add")
    const time = data.get("add_time")
    const type = data.get("add_type")

    const obj = {
        "type": "aggregator",
        "action": "add",
        "form": {
            "name": name,
            "time": time,
            "type": type
        }
    }

    await send_data(obj)
    window.location.reload()
}

async function submit_change(e) {
    e.preventDefault()

    const data = new FormData(e.target)

    const name = data.get("change")
    const time = data.get("ch_time")
    const type = data.get("ch_type")

    const obj = {
        "type": "aggregator",
        "action": "change",
        "form": {
            "name": name,
            "time": time,
            "type": type
        }
    }
    await send_data(obj)
    window.location.reload()
}

async function submit_remove(e) {
    e.preventDefault()

    const data = new FormData(e.target)

    const name = data.get("remove")

    const obj = {
        "type": "aggregator",
        "action": "remove",
        "form": {
            "name": name,
        }
    }
    await send_data(obj)
    window.location.reload()
}


change_form.addEventListener("submit", submit_change)
add_form.addEventListener("submit", submit_add)
remove_form.addEventListener("submit", submit_remove)