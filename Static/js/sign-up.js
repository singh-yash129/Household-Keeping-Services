const container = document.getElementById('container');
const registerBtn = document.getElementById('customer');
const loginBtn = document.getElementById('services');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});