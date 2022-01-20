send_data = async (data) => {
    const location = window.location.href;
    console.log(data) //* i dont think i will ever send some kind of secret data
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
    } catch (e) {
        console.log(e)
    }
}