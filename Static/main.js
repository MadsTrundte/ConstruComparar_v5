document.addEventListener("DOMContentLoaded", function() {
    var backButton = document.getElementById("back-button");
    if (backButton) {
        backButton.addEventListener("click", function() {
            window.history.back();
        });
    }
    var homeButton = document.getElementById("home-button");
    if (homeButton) {
        homeButton.addEventListener("click", function() {
            window.location = "/";
        });
    }
});
