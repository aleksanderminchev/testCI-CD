// document.querySelector('#navn').addEventListener("focus", (e) => {
//   if (document.querySelector('#email-div').classList.contains("hide")){
//     document.querySelector('#email-div').classList.remove('hide');
//   }
// });

// document.querySelector('#email').addEventListener("focus", (e) => {
//   if (document.querySelector('#tlf-div').classList.contains("hide")){
//     document.querySelector('#tlf-div').classList.remove('hide');
//   }
//   if (document.querySelector('#checkboxes-div').classList.contains("hide")){
//     document.querySelector('#checkboxes-div').classList.remove('hide');
//   }
//   if (document.querySelector('#recaptcha').classList.contains("hide")){
//     document.querySelector('#recaptcha').classList.remove('hide');
//   }
// });

// document.querySelector('#tlf').addEventListener("focus", (e) => {
//   if (document.querySelector('#checkboxes-div').classList.contains("hide")){
//     document.querySelector('#checkboxes-div').classList.remove('hide');
//   }
//   if (document.querySelector('#recaptcha').classList.contains("hide")){
//     document.querySelector('#recaptcha').classList.remove('hide');
//   }
// });


document.querySelector('#q1-folkeskole').addEventListener("click", (e) => {
  document.querySelector('#q1').classList.add('contact-inactive');
  document.querySelector('#q2-folkeskole').classList.remove('contact-inactive');
});

document.querySelector('#q1-gym').addEventListener("click", (e) => {
  document.querySelector('#q1').classList.add('contact-inactive');
  document.querySelector('#q2-gym').classList.remove('contact-inactive');
});


const subjects = document.querySelectorAll('.q2-subject');

subjects.forEach(subject => {
  subject.addEventListener('click', function handleClick(event) {
    document.querySelector('#q2-gym').classList.add('contact-inactive');
    document.querySelector('#q2-folkeskole').classList.add('contact-inactive');
    document.querySelector('#q3').classList.remove('contact-inactive');
  });
});



