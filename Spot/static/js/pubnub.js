const pubnub = new PubNub({
    subscribeKey: "sub-c-bd17ee05-352b-4f4b-9a74-d3f91598f507",
    uuid: "flask_app"
});


pubnub.subscribe({
    channels: ["sensor_data"]
});

pubnub.addListener({
    message: function(event) {
        const data = event.message;

        if (data.humidity !== undefined) {
            document.getElementById("humidity").innerText = `${data.humidity.toFixed(1)}%`;
        }
        if (data.temperature_c !== undefined) {
            document.getElementById("temperature").innerText = `${data.temperature_c.toFixed(1)}°`;
        }
    }
});
