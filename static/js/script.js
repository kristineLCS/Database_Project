document.addEventListener('DOMContentLoaded', function() {
    // Home/Index movie slideshow
    let slideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const showSlide = (index) => {
        slides.forEach((slide, i) => {
        slide.style.display = i === index ? 'block' : 'none';
        });
    };
    
    // Show the first slide initially
    showSlide(slideIndex);
    
    // Function to navigate to the next slide
    document.querySelector('.next').addEventListener('click', () => {
        slideIndex = (slideIndex + 1) % slides.length;
        showSlide(slideIndex);
    });
    
    // Function to navigate to the previous slide
    document.querySelector('.prev').addEventListener('click', () => {
        slideIndex = (slideIndex - 1 + slides.length) % slides.length;
        showSlide(slideIndex);
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

            // Toggle the watched class
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
                    
                    // Revert the change in UI
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

                // Revert the change in UI
                this.checked = !isWatched;
                movieItem.classList.toggle('watched', !isWatched);

                setTimeout(() => {
                    statusMessage.textContent = '';
                }, 3000);
            });
        });
    });


    // Select the modal and buttons
    const modal = document.getElementById('confirmation-modal');
    const confirmButton = document.getElementById('confirm-delete');
    const cancelButton = document.getElementById('cancel-delete');
    let movieItemToDelete;

    // Add event listeners to delete buttons
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Store the movie item to delete
            movieItemToDelete = this.closest('.movie-item');
            
            // Show the modal
            modal.style.display = 'flex';
        });
    });

    // Confirm button functionality
    confirmButton.addEventListener('click', function() {
        // Send request to delete the movie (AJAX request)
        const userMovieId = movieItemToDelete.querySelector('.delete-btn').getAttribute('data-user-movie-id');

        fetch('/delete_movie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_movie_id: userMovieId
            })
        })
        .then(response => response.json())
        .then(data => {
            const statusMessage = document.getElementById('status-message');
            if (data.success) {
                // Remove the movie element from the DOM
                movieItemToDelete.remove();
                modal.style.display = 'none';

                statusMessage.textContent = 'Movie deleted successfully.';
                statusMessage.style.color = 'green';
            } else {
                statusMessage.textContent = 'Failed to delete movie.';
                statusMessage.style.color = 'red';
            }
            // Clear the status message after 3 seconds
            setTimeout(() => {
                statusMessage.textContent = '';
            }, 3000);
        });
    });

    // Cancel button functionality
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