document.addEventListener('DOMContentLoaded', function() {
    // Start of sidebar
    const showSidebar = document.getElementById('showsidebar');
    const hideSidebar = document.getElementById('hidesidebar');
    const mySideBar = document.getElementById('mysidebar');


    showSidebar.addEventListener('click', showSidebarBtn);
    function showSidebarBtn() {
        mySideBar.style.width = '250px';
        mySideBar.style.display = 'flex';
    }


    hideSidebar.addEventListener('click', hideSidebarBtn);
    function hideSidebarBtn() {
        mySideBar.style.width = '0';
        mySideBar.style.display = 'none';
    }


    // Sign-up validation
    const signupForm = document.getElementById('signup');
    const email = document.getElementById('email');
    const password = document.getElementById('password');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const formError = document.getElementById('form-error');


    const validation = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;


    if (formError) formError.style.display = 'none';


    if (email) {
        email.addEventListener('input', function() {
            if (validation.test(email.value)) {
                email.classList.add('valid');
                email.classList.remove('invalid');
                emailError.style.display = 'none';
            } else {
                email.classList.add('invalid');
                email.classList.remove('valid');
                emailError.style.display = 'block';
            }
        });
    }


    if (password) {
        password.addEventListener('input', function() {
            if (password.value.length >= 8) {
                password.classList.add('valid');
                password.classList.remove('invalid');
                passwordError.style.display = 'none';
            } else {
                password.classList.add('invalid');
                password.classList.remove('valid');
                passwordError.style.display = 'block';
            }
        });
    }


    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            let inputValid = true;


            if (!validation.test(email.value)) {
                email.classList.add('invalid');
                emailError.style.display = 'block';
                inputValid = false;
            }


            if (password.value.length < 8) {
                password.classList.add('invalid');
                passwordError.style.display = 'block';
                inputValid = false;
            }


            if (!inputValid) {
                event.preventDefault();
                formError.style.display = 'block';
            } else {
                formError.style.display = 'none';
            }
        });
    }

    fetch('/movies')
    .then(response => response.json())
    .then(movies => {
        const moviesContainer = document.getElementById('movies-container');
        movies.forEach(movie => {
            const movieElement = document.createElement('div');
            movieElement.innerHTML = `
                <h2>${movie.title} (${movie.release_year})</h2>
                <p>Genre: ${movie.genre}</p>
                <p>Director: ${movie.director}</p>
                <p>Plot: ${movie.plot}</p>
                <img src="${movie.poster_url}" alt="${movie.title} Poster">
            `;
            moviesContainer.appendChild(movieElement);
        });
    })
    .catch(error => console.error('Error fetching movies:', error));

});

