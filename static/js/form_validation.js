
  // alert('reading form insite invite firends...');

  // Create event field validation
  document.addEventListener('DOMContentLoaded', function () {   
    var form = document.getElementById('myForm');

    function showError(field, errorField, errorMessage) {
      errorField.innerHTML = errorMessage;
      field.classList.add('is-invalid');
    }

    function clearError(field, errorField) {
      errorField.innerHTML = '';
      field.classList.remove('is-invalid');
    }

    function validateName(field, errorField) {
      if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
        var errMsgName = 'Spacific character are not allowed.'
        showError(field, errorField, errMsgName);
        return false;
      } else {
        clearError(field, errorField);
        return true;
      }
    }

    function validateEmailAddress(field, errorField) {
      // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
        var errMsgEmail = 'The email is not in a valid format. Please use a valid email address.'
        showError(field, errorField, errMsgEmail);
        return false;
      } else {
        clearError(field, errorField);
        return true;
      }
    }

    // Create event owner validation
    var eventOwnerInput = form.querySelector('#id_eventOwnerName');
    var eventOwnerError = document.getElementById('eventOwnerName');

    // Create event title validation
    var eventTitleInput = form.querySelector('#id_eventTitle');
    var eventTitleError = document.getElementById('eventTitle');

    // input event listener
    eventOwnerInput.addEventListener('input', function () {
      validateName(eventOwnerInput, eventOwnerError);
    });
    eventTitleInput.addEventListener('input', function () {
      validateName(eventTitleInput, eventTitleError);
    });


  });

  // Registration and update guest field validation
  document.addEventListener('DOMContentLoaded', function () {   
    var form = document.getElementById('myForm');

    function showError(field, errorField, errorMessage) {
      errorField.innerHTML = errorMessage;
      field.classList.add('is-invalid');
    }

    function clearError(field, errorField) {
      errorField.innerHTML = '';
      field.classList.remove('is-invalid');
    }

    function validateName(field, errorField) {
      if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
        var errMsgName = 'Spacific character are not allowed.'
        showError(field, errorField, errMsgName);
        return false;
      } else {
        clearError(field, errorField);
        return true;
      }
    }

    function validateEmailAddress(field, errorField) {
      // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
        var errMsgEmail = 'Email is not valid format.'
        showError(field, errorField, errMsgEmail);
        return false;
      } else {
        clearError(field, errorField);
        return true;
      }
    }

    // Registration event fristName validation
    var firstNameInput = form.querySelector('#id_firstName');
    var firstNameError = document.getElementById('firstName');

    // Registration event lastName validation
    var lastNameInput = form.querySelector('#id_lastName');
    var lastNameError = document.getElementById('lastName');

    // Registration event friendName validation
    var friendNameInput = form.querySelector('#id_friendName');
    var friendNameError = document.getElementById('friendName');

    // Registration email address validation
    var emailAddressInput = form.querySelector('#id_email');
    var emailAddressError = document.getElementById('email');

    // Registration friend email address validation
    var friendEmailAddressInput = form.querySelector('#id_friendEmail');
    var friendEmailAddressError = document.getElementById('friendEmail');

    // input evntListener
    firstNameInput.addEventListener('input', function () {
      validateName(firstNameInput, firstNameError);
    });
    lastNameInput.addEventListener('input', function () {
      validateName(lastNameInput, lastNameError);
    });
    friendNameInput.addEventListener('input', function () {
      validateName(friendNameInput, friendNameError);
    });
    emailAddressInput.addEventListener('input', function () {
      validateEmailAddress(emailAddressInput, emailAddressError);
    });
    
    friendEmailAddressInput.addEventListener('input', function () {
      validateEmailAddress(friendEmailAddressInput, friendEmailAddressError);
    });

  });


  // // User Registration field validation
  // document.addEventListener('DOMContentLoaded', function () {   
  //   var form = document.getElementById('myForm');

  //   function showError(field, errorField, errorMessage) {
  //     errorField.innerHTML = errorMessage;
  //     field.classList.add('is-invalid');
  //   }

  //   function clearError(field, errorField) {
  //     errorField.innerHTML = '';
  //     field.classList.remove('is-invalid');
  //   }

  //   function validateName(field, errorField) {
  //     if (!/^[a-zA-Z\s]+$/.test(field.value.trim())) {
  //       var errMsgName = 'Allow only letter.'
  //       showError(field, errorField, errMsgName);
  //       return false;
  //     } else {
  //       clearError(field, errorField);
  //       return true;
  //     }
  //   }

  //   function validateEmailAddress(field, errorField) {
  //     // !/^[^\s@]+@[^\s@]+\.[^\s@]+$/
  //     if (!/^[0-9a-zA-Z]{1,3}[^\s@]+@[^\s@]+\.[a-zA-Z]{2,3}$/.test(field.value.trim())) {
  //       var errMsgEmail = 'Email is not valid format.'
  //       showError(field, errorField, errMsgEmail);
  //       return false;
  //     } else {
  //       clearError(field, errorField);
  //       return true;
  //     }
  //   }

  //   // Registration event fristName validation
  //   var firstNameInput = form.querySelector('#id_first_name');
  //   var firstNameError = document.getElementById('firstName');

  //   // Registration event lastName validation
  //   var lastNameInput = form.querySelector('#id_last_name');
  //   var lastNameError = document.getElementById('lastName');

  //   // Registration event friendName validation
  //   var emailInput = form.querySelector('#id_email');
  //   var emailError = document.getElementById('email');

  //   // Registration email address validation
  //   var passwordInput1 = form.querySelector('#id_password1');
  //   var passwordError1 = document.getElementById('password1');

  //   // Registration friend email address validation
  //   var passwordInput2 = form.querySelector('#id_password2');
  //   var passwordError2 = document.getElementById('password2');


  //   // input evntListener
  //   firstNameInput.addEventListener('input', function () {
  //     validateName(firstNameInput, firstNameError);
  //   });
  //   lastNameInput.addEventListener('input', function () {
  //     validateName(lastNameInput, lastNameError);
  //   });
  //   emailInput.addEventListener('input', function () {
  //     validateEmailAddress(emailInput, emailError);
  //   });
    


  // });