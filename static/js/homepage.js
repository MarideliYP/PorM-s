$(document).ready(function () {
    let timeout;

    $('.dropend').on({
        "mouseleave": function (){
            if ($(this).find('.dropdown-menu').hasClass("show")) {
                let aux = $(this)
                timeout = setTimeout(function (){
                    aux.click();
                },500);
            }
        },
        "mouseenter": function (){
            clearTimeout(timeout)
        }
    });
});