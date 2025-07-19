
function ajustarClaseCarrito() {
    const pantallaChica = window.matchMedia("(max-width: 985px)");
    const carrito = document.getElementById("carrito");
    const img = document.getElementById("img-carrito");
    const cont = document.getElementById("navbarSupportedContent");
    const carritoDiv = document.getElementById("carrito-div");

    if (pantallaChica.matches) {
        // En pantallas pequeñas
        if (carrito) carrito.classList.remove("submenu");
        if (cont) cont.classList.add("menu");
        if (img) img.classList.add("ulres");

        // Ajustar estilo del carrito
        if (carritoDiv) {
            carritoDiv.style.right = "0";
            carritoDiv.style.left = "auto";
            carritoDiv.style.width = "90%";
        }

    } else {
        // En pantallas grandes
        if (carrito) carrito.classList.add("submenu");
        if (cont) cont.classList.remove("menu");
        if (img) img.classList.remove("ulres");

        // Restablecer estilo original
        if (carritoDiv) {
            carritoDiv.style.right = "20%";
            carritoDiv.style.left = "auto";
            carritoDiv.style.width = "35em";
        }
    }
}

// Llama a la función al cargar
ajustarClaseCarrito();

// Llama a la función al redimensionar
window.addEventListener("resize", ajustarClaseCarrito);