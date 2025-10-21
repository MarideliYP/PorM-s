$(document).ready(function () {
    $('.btn-password').click(function (){

        $(this).find('i').toggleClass('bi-eye-slash bi-eye');

        let eye = $(this).find('i').attr('class');
        if (eye === 'bi bi-eye-slash'){
            $('#password').attr('type', 'password')
        } else {
            $('#password').attr('type', 'text')
        }
    })

    $('.btn-check_pass').click(function (){
        $(this).find('i').toggleClass('bi-eye-slash bi-eye');

        let eye = $(this).find('i').attr('class');
        if (eye === 'bi bi-eye-slash'){
            $('#check_pass').attr('type', 'password')
        } else {
            $('#check_pass').attr('type', 'text')
        }

    })
})
