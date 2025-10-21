document.addEventListener("DOMContentLoaded", function() {
    const formToggleElements = document.querySelectorAll(".form-toggle");
    let activeForm = null; // Variable para rastrear el formulario activo

    formToggleElements.forEach(function(element) {
        element.addEventListener("click", function() {
            const form = this.nextElementSibling;

            if (form === activeForm) {
                // Si el mismo formulario está activo, desactívalo
                form.classList.add("form-hidden");
                activeForm = null;
            } else {
                // Si hay un formulario diferente activo, desactívalo
                if (activeForm) {
                    activeForm.classList.add("form-hidden");
                }

                // Activa el formulario actual
                form.classList.remove("form-hidden");
                activeForm = form;
            }
        });
    });
});


$(document).ready(function() {
    $('#newsForm').submit(function(e) {
        e.preventDefault();// Evita que el formulario se envíe de forma predeterminada

        // Obtén los valores de los campos del formulario
        var title = $('#title').val();
        // Obtén los demás valores de los campos de la noticia
        var url = $('#url').val();
        var fechadepublicacion = $('#publicationDate').val();
        var fuentedepublicacion = $('#publicationSource').val();
        var genero = $('#genre').val();
        var language = $('#language').val();
        var contenido = $('#content').val();
        var imagen = $('#image').val();
        var posturaideologica = $('#ideologicalPosition').val();
        var tematica = $('#topic').val();
        var descriptor = $('#descriptor').val();
        var autores = $('#authors').val();

        // Realiza una petición AJAX al backend para guardar la noticia en la base de datos
        $.ajax({
            url: '/guardar-noticia',
            method: 'POST',
            data: { title: title, url: url, fechadepublicacion: fechadepublicacion, fuentedepublicacion: fuentedepublicacion,
                genero: genero, language: language, contenido: contenido, imagen: imagen, posturaideologica: posturaideologica,
                tematica: tematica, descriptor: descriptor, autores: autores },
            success: function(response) {
                alert("noticia guardada")// Mostrar mensaje de éxito o redireccionar a otra página
            },
            error: function(error) {
                alert("error")// Mostrar mensaje de error o manejar el error de alguna otra manera
            }
        });
    });
});

// Código para el formulario de comentarios y valoraciones

    $(document).ready(function() {
    $('#commentForm').submit(function(e) {
        e.preventDefault();
        // Obtén los valores de los campos del formulario
        var comentario = $('#comment').val();
        var valoracion = $('#rating').val();
        // Obtén los demás valores necesarios para las valoraciones
        var newsId = $('#newsId').val();

        // Realiza una petición AJAX al backend para guardar el comentario y la valoración en la base de datos
        $.ajax({
                url: '/guardar-comentario-valoracion',
                method: 'POST',
                data: { comentario: comentario, valoracion: valoracion, newsId: newsId },
            success: function(response) {
                alert("comentario enviado")// Mostrar mensaje de éxito o actualizar la página para mostrar el nuevo comentario y la valoración
        },
        error: function(error) {
            alert("comentario no enviado")// Mostrar mensaje de error o manejar el error de alguna otra manera
        }
    });
    });
    });


// Código para el formulario de generación de reportes

$(document).ready(function() {
    $('#reportForm').submit(function(e) {
        e.preventDefault();

        // Obtén los valores de los campos del formulario
        var startDate = $('#startDate').val();
        var endDate = $('#endDate').val();
        var tema = $('#theme').val();

        // Realiza una petición AJAX al backend para generar el reporte
        $.ajax({
            url: '/generar-reporte',
            method: 'POST',
            data: { startDate: startDate, endDate: endDate, tema: tema },
            success: function(response) {
                // Mostrar el reporte en el navegador o descargarlo como un archivo
            },
            error: function(error) {
                // Mostrar mensaje de error o manejar el error de alguna otra manera
            }
        });
    });
});










// // Cambiar foto de perfil
// const avatarLink = document.getElementById('avatar-link');
// const avatarInput = document.getElementById('avatar-input');
// const avatarImg = document.getElementById('avatar-img');
//
// // Agrega un evento de clic al enlace de avatar
// avatarLink.addEventListener('click', () => {
//     // Simula hacer clic en el elemento de entrada de archivo (input type="file")
//     avatarImg.click();
// });
//
// // Agrega un evento cuando se selecciona una nueva imagen
// avatarInput.addEventListener('change', (event) => {
//     const selectedImage = event.target.files[1];
//
//     // Verifica si se seleccionó una imagen
//     if (selectedImage) {
//         // Actualiza la imagen de avatar con la imagen seleccionada
//         avatarImg.src = URL.createObjectURL(selectedImage);
//     }
// });