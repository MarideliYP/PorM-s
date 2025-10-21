document.addEventListener('DOMContentLoaded', function () {
    const imgCarrito = document.getElementById('img-carrito');
    const carritoDiv = document.getElementById('carrito-div');
    const carrito = document.getElementById('carrito');

    // Aseguramos que el carrito empiece oculto
    carritoDiv.classList.remove('show');

    // Abrir/cerrar con clic
    imgCarrito.addEventListener('click', function (event) {
        event.stopPropagation();
        if (carritoDiv.classList.contains('show')) {
            carritoDiv.classList.remove('show');
        } else {
            // Aseguramos que no haya múltiples estilos inline
            carritoDiv.style.display = 'block'; // Necesario para que el position: absolute funcione
            carritoDiv.classList.add('show');
        }
    });

    // Cerrar si se hace clic fuera
    document.addEventListener('click', function (event) {
        if (!carrito.contains(event.target)) {
            carritoDiv.classList.remove('show');
        }
    });

    // Evitar cierre al hacer clic dentro del carrito
    carritoDiv.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});

// --- Función responsiva (tu código, ligeramente ajustado) ---
function ajustarClaseCarrito() {
    const pantallaChica = window.matchMedia("(max-width: 985px)").matches;
    const carrito = document.getElementById("carrito");
    const img = document.getElementById("img-carrito");
    const cont = document.getElementById("navbarSupportedContent");
    const carritoDiv = document.getElementById("carrito-div");
    const colortext = document.getElementById("lista-carrito");

    if (pantallaChica) {
        // Modo móvil
        carrito?.classList.remove("submenu");
        colortext?.classList.remove("text-light");
        cont?.classList.add("menu");
        img?.classList.add("ulres");

        // Estilo móvil: carrito como modal
        if (carritoDiv) {
            carritoDiv.style.position = 'fixed';
            carritoDiv.style.top = '80px';
            carritoDiv.style.left = '5%';
            carritoDiv.style.right = 'auto';
            carritoDiv.style.width = '90%';
            carritoDiv.style.maxHeight = 'calc(100vh - 100px)';
            carritoDiv.style.overflowY = 'auto';
        }

    } else {
        // Modo escritorio
        carrito?.classList.add("submenu");
        colortext?.classList.add("text-light");
        cont?.classList.remove("menu");
        img?.classList.remove("ulres");

        // Restaurar estilo original
        if (carritoDiv) {
            carritoDiv.style.position = 'absolute';
            carritoDiv.style.top = '100%';
            carritoDiv.style.right = '0';
            carritoDiv.style.left = 'auto';
            carritoDiv.style.width = '35em';
            carritoDiv.style.maxHeight = 'none';
            carritoDiv.style.overflowY = 'visible';
        }
    }
}

// Ejecutar al cargar y al redimensionar
ajustarClaseCarrito();
window.addEventListener("resize", ajustarClaseCarrito);