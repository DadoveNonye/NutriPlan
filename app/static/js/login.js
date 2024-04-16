// Handles the login section of the code
let icon = document.getElementById("icon");
let password = document.getElementById("password");
icon.addEventListener("click", function () {
  if (password.type === "password") {
    password.type = "text";
    icon.name = "eye-off-outline";
  } else {
    password.type = "password";
    icon.name = "eye-outline";
  }
});
