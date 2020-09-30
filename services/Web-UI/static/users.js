$(document).ready(function () {
    $("#registerForm").submit(function (e) {
        $.ajax({
            type: "POST",
            url: "/register",
            data: JSON.stringify({
                "email": $(this).find("input[name='email']").val(),
                "username": $(this).find("input[name='username']").val(),
                "password": $(this).find("input[name='password']").val()
            }),
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                window.alert(response.message);
            },
            error: function (error) {
                window.alert(error.responseJSON.message);
            }
        });
        e.preventDefault();
    });
});
