/* =====================================================
   GREENFIELD LOCAL HUB - CUSTOM JS (MATCHES YOUR HTML)
===================================================== */


/* =====================================================
   STEP 1 - GET ELEMENTS FROM YOUR HOMEPAGE
===================================================== */

// Your existing inputs (from your HTML)

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const fullNameInput = document.getElementById("fullName");
const phoneInput = document.getElementById("phoneNumber");
const addressInput = document.getElementById("homeAddress");

// Buttons
const registerBtn = document.getElementById("registerBtn");
const signinBtn = document.getElementById("signinBtn");

/* =====================================================
   REGISTER CUSTOMER (UPDATED FOR YOUR FORM)
===================================================== */

registerBtn.addEventListener("click", function () {

    const customerData = {
        email: emailInput.value,
        password: passwordInput.value,
        full_name: fullNameInput.value,
        phone_number: phoneInput.value,
        home_address: addressInput.value
    };

    fetch("http://127.0.0.1:8000/customers", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(customerData)
    })
    .then(res => res.json())
    .then(data => {
        alert("Registered successfully!");

        emailInput.value = "";
        passwordInput.value = "";
        fullNameInput.value = "";
        phoneInput.value = "";
        addressInput.value = "";
    })
    .catch(err => {
        console.error(err);
        alert("Registration failed");
    });

});

// SIGN IN

signinBtn.addEventListener("click", function () {

    const loginData = {
        email: document.getElementById("loginEmail").value,
        password: document.getElementById("loginPassword").value
    };

    fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    })
    .catch(err => {
        console.error(err);
        alert("Sign in failed");
    });

});

