// Navigation Button -  responsive NavBar
const toggleButton = document.querySelector('.toggle-button')
const navBarLinks = document.querySelector('.nav-links')

toggleButton.addEventListener('click', () => {
    navBarLinks.classList.toggle('active');
})

// Alerts set up. Close the alerts when button is clicked.
let alertBtn = document.querySelector('#alert-close-button')
let flashContainer = document.querySelector('.flash-container')

if (alertBtn) {
    flashContainer = document.querySelector('.flash-container')
    alertBtn.addEventListener('click', () => flashContainer.classList.add('flash-container-dismiss'));
}

const flashMessages = (message, category) => {
    flashDiv = document.createElement('div');
    flashDiv.classList.add('flash-container', `flash-container-${category}`);
    messagePara = document.createElement('p');
    messagePara.textContent = message;
    closeIcon = document.createElement('i');
    flashDiv.appendChild(messagePara);
    document.body.appendChild(flashDiv);
    setTimeout(() => { flashDiv.remove(); }, 1000);
  }

