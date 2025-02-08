document.getElementById("registrationForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let selectedLanguage = document.getElementById("language").value;
    window.location.href = selectedLanguage;
});
