// Feedback form submission
document.getElementById('feedback-form').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission behavior

    // Gather the form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    // Process the feedback (e.g., send it to a server or display a success message)
    // For now, we'll just show a success message
    document.getElementById('feedback-response').innerText = 'Thank you for your feedback, ' + name + '!';
    
    // Clear the form fields
    this.reset();
});
