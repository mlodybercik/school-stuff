const change_form = document.getElementById("part-aggregator")
const graph = document.getElementById("graph")

async function submit_change(e) {
    e.preventDefault()

    const data = new FormData(e.target)
    
    const time = data.get("ch_time")
    const agg_type = data.get("ch_agg_type")
    const graph_type = data.get("ch_gra_type")

    const obj = {
        "type": "graphing-aggregator",
        "action": "change",
        "form": {
            "time": time,
            "agg_type": agg_type,
            "graph_type": graph_type
        }
    }

    await send_data(obj)
    window.location.reload()
}

function get_dpi() {
    const temp = document.createElement("div")
    temp.setAttribute("style", "width:1in;visible:hidden;padding:0px")
    document.querySelectorAll("body")[0].appendChild(temp)
    return temp.offsetWidth
}

function calculate_size(dpi, x, y = null) {
    return {"x": Math.floor(x/dpi),  "y": Math.floor(y/dpi)}
}

change_form.addEventListener("submit", submit_change)


get_data = async () => {
    const location = window.location.href + "/graph";
    dpi = get_dpi()
    const data = calculate_size(dpi, graph.clientWidth, 500)
    const settings = {
        method: 'POST',
        headers: {
            'Accept': 'image/svg+xml',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    };

    resposne = await fetch(location, settings)
    graph.innerHTML = await resposne.text()
}

get_data()