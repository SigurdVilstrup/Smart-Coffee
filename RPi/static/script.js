console.log("Document")
var xhr = new XMLHttpRequest();


hour = document.getElementById("hour");
minute = document.getElementById('minute');
button = document.getElementById('time_button');


hour.addEventListener("keydown", sendTime);
minute.addEventListener("keydown", sendTime);

function sendTime(key) {
    if (key.code == 'Enter') {
        setTime()
    }
}

function setTime() {
    if (+(hour.value) >= 0 && +(hour.value) <= 24 && +minute.value >= 0 && +(minute.value) <= 59) {
        location.href = '/time/' + hour.value + '-' + minute.value;
    }

}
