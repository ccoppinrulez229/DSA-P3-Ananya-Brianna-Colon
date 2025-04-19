document.addEventListener('DOMContentLoaded', function() {
    // Retrieve selected genres from localStorage
    const selectedGenres = JSON.parse(localStorage.getItem('selectedGenres')) || [];
    
    // Send request to your Python backend
    fetch('http://localhost:5000/get_recommendations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ genres: selectedGenres }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Get the movie data
        const movies = data.movies;
        
        // Update the HTML elements for each movie
        for (let i = 0; i < Math.min(movies.length, 3); i++) {
            const movie = movies[i];
            
            // Get the relevant result box (assuming you have 3)
            const resultBox = document.querySelectorAll('.results-box')[i+1]; // +1 because first box is the header
            
            // Update the title
            resultBox.querySelector('h2').textContent = movie.title;
            
            // Update the rating
            resultBox.querySelector('#rating').textContent = movie.rating;
            
            // Update the genres
            resultBox.querySelector('#genres').textContent = movie.genres.join(', ');
            
            // Update poster if available
            if (movie.posterUrl) {
                resultBox.querySelector('#poster').src = movie.posterUrl;
            }
        }
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
        // Display some error message on the page
    });
});