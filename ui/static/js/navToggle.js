const toggleButton = document.querySelector('.toggle-button')
const navBarLinks = document.querySelector('.nav-links')

toggleButton.addEventListener('click', () => {
    navBarLinks.classList.toggle('active');
})