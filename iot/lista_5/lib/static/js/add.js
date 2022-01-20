const form = document.getElementById("add")

async function submit(e) {
    e.preventDefault()
    const data = new FormData(e.target);

    const obj = {
        "address": data.get("address"),
        "name": data.get("name")
    }
    console.log(obj)
    if (await send_data(obj)) {
        const protocol = window.location.protocol
        const host = window.location.host
        window.location.href = "/"
    }
}

send_data = async (data) => {
    const location = window.location.href;
    const settings = {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    };
    try {
        await fetch(location, settings);
        return true
    } catch (e) {
        return false
        console.log(e)
    }

}

form.addEventListener("submit", submit)