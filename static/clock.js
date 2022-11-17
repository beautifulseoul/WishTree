const clock = document.querySelector('h2#clock');



function getClock() {
    const date = new Date();
    // clock.innerText = (`${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`)
    const hours = String(date.getHours()).padStart(2,'0');
    const minutes = String(date.getMinutes()).padStart(2,'0');
    // const seconds = String(date.getSeconds()).padStart(2,'0');

    clock.innerText = `${hours}:${minutes}`
}

getClock(); //1초뒤가 아닌 page를 열면 바로 시작될 수 있도록. 
setInterval(getClock,60000)