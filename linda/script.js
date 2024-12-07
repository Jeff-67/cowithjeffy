$(document).ready(function () {
    // Add employee functionality
    $("#add-employee form").submit(function (event) {
        event.preventDefault(); // Prevent default form submission
        const employeeName = $("#employee-name").val();

        if (employeeName.trim() !== "") {
            // Send AJAX request to add employee to the server
            $.ajax({
                url: "/add_employee",
                method: "POST",
                data: { employee: employeeName },
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
        // Send AJAX request to select a winner
        $.ajax({
            url: "/select_winner",
            method: "GET",
            success: function (response) {
                if (response.winner) {
                    // Update the winner announcement
                    $("#winner-announcement").text(`Congratulations, ${response.winner}!`);
                } else {
                    alert(response.message || "No winner could be selected.");
                }
            },
            error: function () {
                alert("Error selecting winner.");
            },
        });
    });

    // Clear candidates functionality
    $("#clear-candidates").click(function (event) {
        event.preventDefault(); // Prevent default behavior if it's inside a form
        if (confirm('Are you sure you want to reset all candidates? This action cannot be undone.')) {
            fetch('/clear_candidates', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.success) {
                        // Clear the employee list on the frontend
                        $("#employee-list ul").empty();
                        alert(data.message || 'All candidates have been reset.');
                    } else {
                        alert('Error resetting candidates: ' + (data.message || 'Unknown error'));
                    }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('Error resetting candidates.');
                });
        }
    });
});
