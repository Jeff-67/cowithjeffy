$(document).ready(function () {
    // Add employee functionality
    $("#add-employee form").submit(function (event) {
        event.preventDefault(); // Prevent default form submission
        const employeeName = $("#employee-name").val();
    
        if (employeeName.trim() !== "") {
            // Send AJAX request to add employee to the server
            $.ajax({
                url: "/add_employees", // Use the plural endpoint name
                method: "POST",
                contentType: "application/json", // Ensure JSON format
                data: JSON.stringify({ names: [employeeName] }), // Wrap name in an array
                success: function (response) {
                    if (response.success) {
                        // Update the employee list
                        $("#employee-list ul").append(`<li>${employeeName}</li>`);
                        $("#employee-name").val(""); // Clear input field
                    } else {
                        alert(response.message || "Error adding employee.");
                    }
                },
                error: function () {
                    alert("Error adding employee.");
                },
            });
        } else {
            alert("Please enter an employee name.");
        }
    });

    // Lottery functionality
    $("#select-winner").click(function () {
        const prizeType = $("#prize-type").val(); // Assuming a dropdown for prize type
        const numWinners = $("#num-winners").val(); // Input for number of winners
    
        if (!prizeType || !numWinners) {
            alert("Please provide both prize type and number of winners.");
            return;
        }
    
        // Send AJAX request to select winners
        $.ajax({
            url: `/select_winner?prize_type=${prizeType}&num_winners=${numWinners}`,
            method: "GET",
            success: function (response) {
                if (response.winners) {
                    const winnerList = response.winners
                        .map(winner => `<li>${winner}</li>`)
                        .join("");
                    $("#winner-announcement").html(
                        `<p>Congratulations to the winners:</p><ul>${winnerList}</ul>`
                    );
                } else {
                    alert(response.error || "No winner could be selected.");
                }
            },
            error: function () {
                alert("Error selecting winners.");
            },
        });
    });

    $("#reset-winners").click(function () {
        if (confirm("Are you sure you want to reset all winners?")) {
            $.ajax({
                url: "/reset_winners",
                method: "POST",
                success: function (response) {
                    if (response.success) {
                        alert(response.message);
                    } else {
                        alert("Error resetting winners: " + response.message);
                    }
                },
                error: function () {
                    alert("Error resetting winners.");
                },
            });
        }
    });

    // Clear candidates functionality
    $("#clear-candidates").click(function (event) {
        event.preventDefault(); // Prevent default behavior
        if (confirm("Are you sure you want to reset all candidates? This action cannot be undone.")) {
            $.ajax({
                url: "/clear_candidates",
                method: "POST",
                success: function (response) {
                    if (response.success) {
                        // Clear the employee list on the frontend
                        $("#employee-list ul").empty();
                        alert(response.message || "All candidates have been reset.");
                    } else {
                        alert("Error resetting candidates: " + (response.message || "Unknown error"));
                    }
                },
                error: function () {
                    alert("Error resetting candidates.");
                },
            });
        }
    });
    
});
