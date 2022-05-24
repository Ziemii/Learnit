// Password field length check
document.getElementById("password").addEventListener("keyup", function () {
    if (document.getElementById("password").value.length < 4) {
      document.getElementById("password").style.backgroundColor = "#ffcfcf";
      //   formStatus[1] = 0;
      //   checkForm();
    } else {
      document.getElementById("password").style.backgroundColor = "#fff";
      //   formStatus[1] = 1;
      //   checkForm();
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
        // formStatus[2] = 0;
        // checkForm();
      } else {
        document.getElementById("confirmPassword").style.backgroundColor = "#fff";
        document.getElementById("changebtn").disabled = false;
        // formStatus[2] = 1;
        // checkForm();
      }
    });