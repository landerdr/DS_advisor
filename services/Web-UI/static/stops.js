$(document).ready(function () {
    $("#select-stop").on("change", function (e) {
        let entity_number = $("option:selected", this).attr("entity_number");
        let stop_number = $("option:selected", this).attr("stop_number");

        if (!entity_number && !stop_number)
            return;

        $.ajax({
            type: "GET",
            url: `/stop/${entity_number}/${stop_number}`,
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                document.getElementById("stop_info").innerHTML =
                    `<h3> ${response.data.entity_number} ${response.data.stop_number} </h3>
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

    $("#rateStop").on("submit", function (e) {
        let entity_number = $("option:selected", $("#select-stop")).attr("entity_number");
        let stop_number = $("option:selected", $("#select-stop")).attr("stop_number");

        if (!entity_number && !stop_number)
            return window.alert("Please select a stop before trying to add your rating");

        $.ajax({
            type: "POST",
            url: `/stop/rate`,
            data: JSON.stringify({
                "entity_number": parseInt(entity_number),
                "stop_number": parseInt(stop_number),
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

    $("#deleteStopRating").on("submit", function (e) {
        let entity_number = $("option:selected", $("#select-stop")).attr("entity_number");
        let stop_number = $("option:selected", $("#select-stop")).attr("stop_number");

        if (!entity_number && !stop_number)
            return window.alert("Please select a stop before trying to remove your rating");

        $.ajax({
            type: "DELETE",
            url: `/stop/rate`,
            data: JSON.stringify({
                "entity_number": parseInt(entity_number),
                "stop_number": parseInt(stop_number),
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

    $("#linestops").on("click", function (e) {
        let entity_number = $("option:selected", $("#select-line")).attr("entity_number");
        let line_number = $("option:selected", $("#select-line")).attr("line_number");
        let direction = $("option:selected", $("#select-line")).attr("direction");

        if (!entity_number && !line_number && !direction)
            return window.alert("Please select a line before trying to move on");

        window.location.replace(`/stops/line/${entity_number}/${line_number}/${direction}`);

        e.preventDefault()
    });

    $("#townstops").on("click", function (e) {
        let town_id = $("option:selected", $("#select-town")).attr("town_id");

        if (!town_id)
            return window.alert("Please select a town before trying to move on");

        window.location.replace(`/stops/town/${town_id}`);

        e.preventDefault()
    });
});
