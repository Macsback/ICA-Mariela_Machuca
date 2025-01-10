
// Pubnub info in real time
const pubnub = new PubNub({
    subscribeKey: "sub-c-bd17ee05-352b-4f4b-9a74-d3f91598f507",
    publish_key : "pub-c-a1bfc69b-5a49-4f45-9a35-d0177b206c7e" ,
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

//Timer Logic
let chronometerInterval;
let chronometerTime = 0; 

function formatTime(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return [hrs, mins, secs]
        .map((val) => (val < 10 ? `0${val}` : val))
        .join(":");
}

function startChronometer() {
    if (!chronometerInterval) {
        chronometerInterval = setInterval(() => {
            chronometerTime++;
            document.getElementById("timer").innerText = formatTime(chronometerTime);

        
            Alert(chronometerTime);
        }, 1000);
    }
}


function stopChronometer() {
    clearInterval(chronometerInterval);
    chronometerInterval = null;
}


function resetChronometer() {
    stopChronometer();
    chronometerTime = 0;
    document.getElementById("messageDisplay").innerText = " "
    document.getElementById("timer").innerText = "00:00:00";
}

function Alert(chronometerTime) {

chronometerTime = chronometerTime/60;


    const cookingTime = parseInt(
        document.getElementById("cookingTime").dataset.time);

    const actTemperature = parseFloat(
            document.getElementById("temperature").dataset.temperature);

    const perfeTemperature = parseFloat(
                document.getElementById("perfTemperature").dataset.perftemp); //data-set is case Sensitive!!

    const actHumid = parseFloat(
                    document.getElementById("humidity").dataset.humidity);

    const perfHumid = parseFloat(
                    document.getElementById("perfHumidity").dataset.perfhumid);

   // console.log(cookingTime)
    //console.log(actTemperature)
    //console.log(perfeTemperature)
   // console.log(actHumid)
    //console.log(perfHumid)

    if (chronometerTime === cookingTime || actTemperature === perfeTemperature || actHumid === perfHumid) {
        pubnub.publish({
            channel: "sensor_data",
            message: { text: "Food is Ready!" }
        }, function(status, response) {
            if (status.error) {
                console.error("Error sending PubNub message:", status);
            } else {
                console.log("Alert message sent:", response);
            }
        });

        document.getElementById("messageDisplay").innerText = "Food is Ready!"
    }
}
document.getElementById("start-timer").addEventListener("click", startChronometer);
document.getElementById("stop-timer").addEventListener("click", stopChronometer);
document.getElementById("reset-timer").addEventListener("click", resetChronometer);