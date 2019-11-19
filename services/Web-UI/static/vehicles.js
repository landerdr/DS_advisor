$(document).ready(function () {
    $("#addVehicle").submit(function (e) {
        $.ajax({
            type: "POST",
            url: "/vehicle",
            data: JSON.stringify({
                "email": $(this).find("input[name='email']").val(),
                "password": $(this).find("input[name='password']").val(),
                "entity_number": parseInt($(this).find("input[name='entity_number']").val()),
                "vehicle_number": parseInt($(this).find("input[name='vehicle_number']").val()),
                "vehicle_type": parseInt($("option:selected", $(this).find("select[name='vehicle_type']")).attr("value"))
            }),
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                window.alert(response.message);
                window.location.reload()
            },
            error: function (error) {
                window.alert(error.responseJSON.message);
            }
        });
        e.preventDefault();
    });

    $("#select-vehicle").on("change", function (e) {
        let id = $("option:selected", this).attr("id");
        $.ajax({
            type: "GET",
            url: `/vehicle/${id}`,
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                document.getElementById("vehicle_info").innerHTML =
                    `<h3> ${response.data.entity_number} ${response.data.vehicle_number} </h3>
                    <h6> Scores: ${response.data.ratings.length === 0 ? "not yet scored" : response.data.ratings.join(" ")} </h6>
                    <h6> Average score: ${(response.data.avg_rating)} </h6>
                    `;
            },
            error: function (error) {
                window.alert(error.responseJSON.message);
            }
        });
        e.preventDefault();
    });

    $("#rateVehicle").on("submit", function (e) {
        let id = $("option:selected", $("#select-vehicle")).attr("id");
        $.ajax({
            type: "POST",
            url: `/vehicle/rate`,
            data: JSON.stringify({
                "vehicle_id": id,
                "email": $(this).find("input[name='email']").val(),
                "password": $(this).find("input[name='password']").val(),
                "rating": parseInt($(this).find("input[name='rating']").val())
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

    $("#deleteVehicle").on("submit", function (e) {
        let id = $("option:selected", $("#select-vehicle")).attr("id");
        $.ajax({
            type: "DELETE",
            url: `/vehicle`,
            data: JSON.stringify({
                "vehicle_id": id,
                "email": $(this).find("input[name='email']").val(),
                "password": $(this).find("input[name='password']").val()
            }),
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                window.alert(response.message);
                window.location.reload();
            },
            error: function (error) {
                window.alert(error.responseJSON.message);
            }
        });
        e.preventDefault();
    });

    $("#deleteVehicleRating").on("submit", function (e) {
        let id = $("option:selected", $("#select-vehicle")).attr("id");
        $.ajax({
            type: "DELETE",
            url: `/vehicle/rate`,
            data: JSON.stringify({
                "vehicle_id": id,
                "email": $(this).find("input[name='email']").val(),
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
