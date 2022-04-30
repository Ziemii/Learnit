let email = document.getElementById("email");

// Non-empty username field check
document
  .getElementById("username")
  .addEventListener("focusout", function () {
    if (
      document.getElementById("username").value == ''
    ) {
      document.getElementById("username").style.backgroundColor =
        "#ffcfcf";
    } else {
      document.getElementById("username").style.backgroundColor = "#fff";
    }
  });





// Password equality check
document
  .getElementById("confirmPassword")
  .addEventListener("keyup", function () {
    if (
      document.getElementById("password").value !=
      document.getElementById("confirmPassword").value
    ) {
      document.getElementById("confirmPassword").style.backgroundColor =
        "#ffcfcf";
    } else {
      document.getElementById("confirmPassword").style.backgroundColor = "#fff";
    }
  });
