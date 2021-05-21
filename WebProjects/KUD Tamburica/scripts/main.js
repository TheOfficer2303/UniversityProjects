let burgerKing = document.getElementById("burger");
let menu = document.getElementById("menu");
let mediaQuery = window.matchMedia("(max-width:768px)");

let left = document.getElementById("lijevo");
let right = document.getElementById("desno");
let images = document.getElementById("images");

let toggle = 0;
let shiftedRight = 0;
let shiftedLeft = 0;

burgerKing.onclick = openBurger;
mediaQuery.addListener(normalize);

left.onclick = slideLeft;
right.onclick = slideRight;

function slideLeft() {
    if (shiftedRight) {
        images.style.transform = "translateX(0%)";
        shiftedRight = 0;
    } else {
        images.style.transform = "translateX(-100%)";
        shiftedLeft = 1;
    }
    
}

function slideRight() {
    if (shiftedLeft) {
        images.style.transform = "translateX(0%)";
        shiftedLeft = 0;
    } else {
        images.style.transform = "translateX(100%)";
        shiftedRight = 1;
    }
    
}

function openBurger() {
    if (window.matchMedia("(max-width:768px)")) {
        if (toggle == 0) {
            menu.style.transform = "translateX(0%)"
            toggle = 1;
            burgerKing.style.backgroundColor = "rgb(194, 193, 193)";
            burgerKing.style.border = "1px solid black"
            burgerKing.style.borderRadius = "3px";
        } else {
            menu.style.transform = "translateX(-100%)";
            toggle = 0;
            burgerKing.style.backgroundColor = "";
            burgerKing.style.border = "none";

        }
    } 
}

function normalize(e) {
    if (!e.matches) {
        menu.style.transform = "translateX(0%)";
        toggle = 1;
    }
}