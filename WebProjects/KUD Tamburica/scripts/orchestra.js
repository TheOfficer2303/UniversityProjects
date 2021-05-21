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


0|0,2,0|1,2,0
q1,q2,q3
0,1,2
J,N,K
q3
q1
K
q1,0,K->q1,NK
q1,1,K->q1,JK
q1,0,N->q1,NN
q1,1,N->q1,JN
q1,0,J->q1,NJ
q1,1,J->q1,JJ
q1,2,K->q2,K
q1,2,N->q2,N
q1,2,J->q2,J
q2,0,N->q2,$
q2,1,J->q2,$
q2,$,K->q3,$

