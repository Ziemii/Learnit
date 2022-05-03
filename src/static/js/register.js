let email = document.getElementById("email");

//Regular expression for email check
const reMail = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
var formStatus = [0, 0, 0, 0, 0];

// Initial check to disable button
checkForm();

// Non-empty username field check
document.getElementById("username").addEventListener("keyup", function () {
  if (document.getElementById("username").value.length < 2) {
    document.getElementById("username").style.backgroundColor = "#ffcfcf";
    formStatus[0] = 0;
    checkForm();
  } else {
    document.getElementById("username").style.backgroundColor = "#fff";
    formStatus[0] = 1;
    checkForm();
  }
});

// Password field length check
document
  .getElementById("password")
  .addEventListener("keyup", function () {
    if (
      document.getElementById("password").value.length < 4 ) {
      document.getElementById("password").style.backgroundColor =
        "#ffcfcf";
      formStatus[1] = 0;
      checkForm();
    } else {
      document.getElementById("password").style.backgroundColor = "#fff";
      formStatus[1] = 1;
      checkForm();
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
      formStatus[2] = 0;
      checkForm();
    } else {
      document.getElementById("confirmPassword").style.backgroundColor = "#fff";
      formStatus[2] = 1;
      checkForm();
    }
  });

// Email validation
document.getElementById("email").addEventListener("keyup", function () {
  let text = document.getElementById("email").value;
  let result = text.match(reMail);
  if (!result) {
    document.getElementById("email").style.backgroundColor = "#ffcfcf";
    formStatus[3] = 0;
    checkForm();
  } else {
    document.getElementById("email").style.backgroundColor = "#fff";
    formStatus[3] = 1;
    checkForm();
  }
});

//Terms check
document
  .querySelector("input[name=terms]")
  .addEventListener("change", function () {
    if (this.checked) {
      formStatus[4] = 1;
      checkForm();
    } else {
      formStatus[4] = 0;
      checkForm();
    }
  });

// Check if every form field is valid 
function checkForm() {
  if (
    formStatus.reduce(
      (previousValue, currentValue) => previousValue + currentValue,
      0
    ) == 5
  ) {
    document.getElementById("registerbtn").disabled = false;
  } else {
    document.getElementById("registerbtn").disabled = true;
  }
}

