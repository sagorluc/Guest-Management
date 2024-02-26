// Function to show the popup
function showPopup() {
    document.getElementById('popup').style.display = 'block';
}

// Function to hide the popup
function hidePopup() {
    document.getElementById('popup').style.display = 'none';
}

// Attach event listener to form submission
document.getElementById('popupForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission
    // Process input values (e.g., send to server)
    const name = document.getElementById('friend_name').value;
    const email = document.getElementById('friend_email').value;
    console.log('Name:', name);
    console.log('Email:', email);
    // Hide the popup
    hidePopup();
});

// Listen for input events on the threshold input field
document.getElementById('id_totalPerson').addEventListener('input', function(event) {
    const value = parseFloat(event.target.value);
    if (value > 1) {
        showPopup();
    } else {
        hidePopup();
    }
});

  