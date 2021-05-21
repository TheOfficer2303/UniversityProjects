players = document.getElementsByClassName("player");
info = document.getElementsByClassName("player-hidden");
let toggle = 0; //ZATVORENO
for (const element of players) {
    console.log(element);
}

for (const element of info) {
    console.log(element);
    element.style.display = "none";
}

for (let i = 0; i < players.length; i++) {
    const element = players[i];
    const content = info[i];
    element.addEventListener("click", function() {
        for (const otherEl of info) {
            if (otherEl !== info[i] && otherEl.style.display === "block") {
                otherEl.style.display = "none";
            }
        }
    
        if (content.style.display === "block") {
            toggle = 0;
            content.style.display = "none";
        } else {
            toggle = 1;
            content.style.display = "block";
        }
    })
    content.addEventListener("click", function() {
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    })
}
