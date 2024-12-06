$(document).ready(function() {
    // Add employee functionality
    $("#add-employee form").submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        const employeeName = $("#employee-name").val();

        if (employeeName.trim() !== "") {
            // Send AJAX request to add employee to the server
            $.ajax({
                url: "/add_employee",
                method: "POST",
                data: { employee: employeeName },
                success: function(response) {
                    // Update the employee list
                    $("#employee-list ul").append(`<li>${employeeName}</li>`);
                    $("#employee-name").val(""); // Clear input field
                },
                error: function() {
                    alert("Error adding employee.");
                }
            });
        } else {
            alert("Please enter an employee name.");
        }
    });

    // Lottery functionality
    $("#select-winner").click(function() {
        // Send AJAX request to select a winner
        $.ajax({
            url: "/select_winner",
            method: "GET",
            success: function(response) {
                // Update the winner announcement
                $("#winner-announcement").text(`Congratulations, ${response}!`);
            },
            error: function() {
                alert("Error selecting winner.");
            }
        });
    });
});