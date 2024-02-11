let numberOfItems = document.getElementById("cart-items");
numberOfItems.textContent = localStorage.getItem("cart-items")

if (!numberOfItems.textContent) {
    numberOfItems.textContent = 0;
    localStorage.setItem("cart-items", numberOfItems.textContent);
}




