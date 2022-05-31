// Password field length check
document.getElementById("password").addEventListener("keyup", function () {
    if (document.getElementById("password").value.length < 4) {
      document.getElementById("password").style.backgroundColor = "#ffcfcf";
    } else {
      document.getElementById("password").style.backgroundColor = "#fff";
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
        document.getElementById("changebtn").disabled = false;
      }
    });