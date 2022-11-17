const API_KEY = 'cf8526a878dd773b581b5fc4013a09c3';


function onGeoSucc(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    // console.log(lat, lng)
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${API_KEY}&units=metric`
    // console.log(url);
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const temp = document.querySelector("#weather span:first-child")
            const weather = document.querySelector("#weather span:nth-child(2)");
            const city = document.querySelector("#weather span:nth-child(3)");
            
            // const icon = document.querySelector("img[src='https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png']")
            city.innerText = data.name;
            weather.innerText = data.weather[0].main;

            const temp_num = Math.ceil(data.main.temp);
            temp.innerText = `${temp_num}℃`;
            

            const weatherIcon = document.querySelector("#weather img");
            const weatherIconCode = data.weather[0].icon;
            // weatherIcon.src = `/img/icons/${weatherIconCode}.png/`;
            weatherIcon.src = `https://openweathermap.org/img/wn/${weatherIconCode}@2x.png`


            
            
    })
}
[0]

function onGeoError() {
    alert("Can't find you. No weather for you.")
}


navigator.geolocation.getCurrentPosition(onGeoSucc, onGeoError)