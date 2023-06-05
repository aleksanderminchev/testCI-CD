//-----------------------//
// ---- PHONE INPUT ---- //
//-----------------------//

const phoneInputField = document.querySelectorAll("form #tlf");
const submitButtons = document.querySelectorAll("form .tt__btn");
const validationMessages = document.querySelectorAll(".validation_message");
const fulltlf = document.querySelectorAll("#fulltlf");
const inputForms = document.querySelectorAll("form");

const phoneInput = [];

for (let i = 0; i < phoneInputField.length; i++) {
  phoneInput[i] = window.intlTelInput(phoneInputField[i], {
    preferredCountries: ["dk", "fo", "gl"],
    utilsScript:
      "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
    autoPlaceholder: "aggressive",
  });
}

const countryDropdowns = document.querySelectorAll(".iti__selected-flag");

for (let i = 0; i < phoneInputField.length; i++) {
  // Input
  phoneInputField[i].addEventListener("input", () => handlePhoneInput(i));
  // Blur
  phoneInputField[i].addEventListener("blur", (e) => handlePhoneBlur(e, i));
  // countryDropdown click
  countryDropdowns[i].addEventListener("click", () => {
    validationMessages[i].classList.add("hidden");
  });
  // Country change
  phoneInputField[i].addEventListener("countrychange", handleCountryChange(i));
  // s[i].addEventListener("click", indexHeroFormSubmit(i));
}
function handlePhoneInput(index) {
  validationMessages[index].classList.add("hidden");
  //submitButtons[index].style.opacity = phoneInput[index].isValidNumber()
  //  ? "1"
  //  : "0.5";
}

function handlePhoneBlur(event, index) {
  if (phoneInput[index].isValidNumber()) {
    isValid(index);
  } else if (
    event.relatedTarget &&
    event.relatedTarget.className === "iti__selected-flag"
  ) {
    validationMessages[index].classList.add("hidden");
  } else if (phoneInputField[index].value.length === 0) {
    validationMessages[index].classList.add("hidden");
  } else {
    isInvalid(index);
  }
}

function handleCountryChange(index) {
  validationMessages[index].classList.add("hidden");
}

function isValid(index) {
  //submitButtons[index].style.opacity = "1";
  validationMessages[index].classList.add("hidden");
  fulltlf[index].value = phoneInput[index].getNumber();
}

function isInvalid(index) {
  //submitButtons[index].style.opacity = "0.5";
  validationMessages[index].classList.remove("hidden");
}

//  Send information
// hero form
function indexHeroFormSubmit() {
  submitPhoneNumber();
}

// cta1
function ctaPhoneFormSubmit() {
  submitPhoneNumber();
}

// cta2
function ct2PhoneFormSubmit() {
  submitPhoneNumber();
}

// kontakt page
function contactFormSubmit() {
  submitPhoneNumber();
}

function submitPhoneNumber() {
  for (let i = 0; i < phoneInput.length; i++) {
    if (phoneInputField[i].value !== "" && phoneInput[i].isValidNumber()) {
      inputForms[i].submit();
    }
  }
}
