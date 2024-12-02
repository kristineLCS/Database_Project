document.addEventListener('DOMContentLoaded', function() {
    // Start of sidebar
    const sidebar = document.getElementById('mysidebar');
    const showSidebarBtn = document.getElementById('showsidebar');
    const hideSidebarBtn = document.getElementById('hidesidebar');
    

    // Show the sidebar
    showSidebarBtn.addEventListener('click', () => {
        sidebar.classList.add('open');
        sidebar.style.width = '250px';
        sidebar.style.display = 'flex';
    });

    // Hide the sidebar
    hideSidebarBtn.addEventListener('click', () => {
        sidebar.classList.remove('open');
        sidebar.style.width = '0';
        sidebar.style.display = 'none';
    });
    
    
    // Home/Index movie slideshow
    let mainSlideIndex = 0;
    const mainSlides = document.querySelectorAll('.slideshow-container .slide');

    const showMainSlide = (index) => {
        mainSlides.forEach((slide, i) => {
            slide.style.display = i === index ? 'block' : 'none';
        });
    };

    // Show the first slide initially
    showMainSlide(mainSlideIndex);

    // Navigate to the next slide
    document.querySelector('.prev').addEventListener('click', () => {
        mainSlideIndex = (mainSlideIndex - 1 + mainSlides.length) % mainSlides.length;
        showMainSlide(mainSlideIndex);
    });

    // Navigate to the previous slide
    document.querySelector('.next').addEventListener('click', () => {
        mainSlideIndex = (mainSlideIndex + 1) % mainSlides.length;
        showMainSlide(mainSlideIndex);
    });


    const genres = ['romance', 'drama', 'action', 'comedy'];

    genres.forEach(genre => {
        let genreSlideIndex = 0;
        const genreSlides = document.querySelectorAll(`#${genre}-slideshow .genre-slide`);
        const prevButton = document.querySelector(`.prevbtn[data-genre="${genre}"]`);
        const nextButton = document.querySelector(`.nextbtn[data-genre="${genre}"]`);

        if (genreSlides.length === 0) {
            // Hide navigation buttons if no slides exist
            if (prevButton) prevButton.style.display = 'none';
            if (nextButton) nextButton.style.display = 'none';
            return;
        }

        function showGenreSlide() {
            genreSlides.forEach((slide, index) => {
                slide.style.display = index === genreSlideIndex ? 'block' : 'none';
            });
        }

        prevButton.addEventListener('click', () => {
            genreSlideIndex = (genreSlideIndex - 1 + genreSlides.length) % genreSlides.length;
            showGenreSlide();
        });

        nextButton.addEventListener('click', () => {
            genreSlideIndex = (genreSlideIndex + 1) % genreSlides.length;
            showGenreSlide();
        });

        // Initialize the first slide
        showGenreSlide();
    });
        
    
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


    // Add an event listener to all buttons with the class 'add-btn'
    document.querySelectorAll('.add-btn').forEach(button => {
        button.addEventListener('click', function (event) {
            // Check if the button's 'data-authenticated' attribute is set to 'true'
            const isAuthenticated = this.getAttribute('data-authenticated') === 'true';
    
            // If the user is not authenticated, display a message
            if (!isAuthenticated) {
                // Get or create the <p> element for the message
                let messageElement = document.getElementById('auth-message');
                
                if (!messageElement) {
                    // Create and style the message element
                    messageElement = document.createElement('p');
                    messageElement.id = 'auth-message';
                    messageElement.style.color = 'red';
                    messageElement.style.fontWeight = 'bold';
                    document.querySelector('.alert').appendChild(messageElement);
                }
    
                // Set the message and make it visible
                messageElement.textContent = "You need to log in to add movies to your list.";
                messageElement.style.display = 'block';
    
                // Hide the message after a few seconds
                setTimeout(() => {
                    messageElement.style.display = 'none';
                }, 3000);
    
                // Prevent any further actions
                event.preventDefault();
            }
        });
    });
    
    // Handle the change event on the checkbox to mark as watched/unwatched
    document.querySelectorAll('.watched-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function () {
            const movieItem = this.closest('.movie-item');
            const userMovieId = this.getAttribute('data-user-movie-id');
            const isWatched = this.checked;

            // Add a console log for debugging
            console.log(`Checkbox change detected for movie ID: ${userMovieId}, watched status: ${isWatched}`);

            // Toggle the watched class
            if (movieItem) {
                movieItem.classList.toggle('watched', isWatched);

                // Send the update to the server
                fetch('/update_watched_status', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_movie_id: userMovieId,
                        watched: isWatched
                    })
                })
                .then(response => response.json())
                .then(data => {
                    const statusMessage = document.getElementById('status-message');
                    if (data.success) {
                        statusMessage.textContent = 'Status updated successfully.';
                        statusMessage.style.color = 'green';
                    } else {
                        statusMessage.textContent = 'Failed to update status.';
                        statusMessage.style.color = 'red';

                        // Revert the change in UI if failed
                        this.checked = !isWatched;
                        movieItem.classList.toggle('watched', !isWatched);
                    }
                    setTimeout(() => {
                        statusMessage.textContent = '';
                    }, 3000);
                })
                .catch(() => {
                    const statusMessage = document.getElementById('status-message');
                    statusMessage.textContent = 'An error occurred. Please try again.';
                    statusMessage.style.color = 'red';

                    // Revert the change in UI if failed
                    this.checked = !isWatched;
                    movieItem.classList.toggle('watched', !isWatched);

                    setTimeout(() => {
                        statusMessage.textContent = '';
                    }, 3000);
                });
            } else {
                console.error('Movie item not found.');
            }
        });
    });

    // Confirm button functionality for deleting a movie
    const modal = document.getElementById('confirmation-modal');
    const confirmButton = document.getElementById('confirm-delete');
    const cancelButton = document.getElementById('cancel-delete');
    let movieItemToDelete;

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            movieItemToDelete = this.closest('.movie-item');
            if (movieItemToDelete) {
                modal.style.display = 'block'; // Ensure modal shows correctly
            } else {
                console.error('Movie item not found for deletion.');
            }
        });
    });

    confirmButton.addEventListener('click', function() {
        const userMovieId = movieItemToDelete.querySelector('.delete-btn').getAttribute('data-user-movie-id');

        fetch('/delete_movie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_movie_id: userMovieId })
        })
        .then(response => response.json())
        .then(data => {
            const statusMessage = document.getElementById('status-message');
            if (data.success) {
                movieItemToDelete.remove();
                modal.style.display = 'none';

                statusMessage.textContent = 'Movie deleted successfully.';
                statusMessage.style.color = 'green';
            } else {
                statusMessage.textContent = 'Failed to delete movie.';
                statusMessage.style.color = 'red';
            }
            setTimeout(() => {
                statusMessage.textContent = '';
            }, 3000);
        })
        .catch(error => {
            console.error('Error deleting movie:', error);
        });
    });

    cancelButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Hides flash messages after 3 seconds
    const flashMessages = document.querySelectorAll('.flash-messages li');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.display = 'none';
        }, 3000);  // 3000 milliseconds = 3 seconds
    });
    
});