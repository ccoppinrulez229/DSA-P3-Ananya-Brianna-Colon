document.addEventListener('DOMContentLoaded', function () {
    const selectedGenres = JSON.parse(localStorage.getItem('selectedGenres')) || [];
    const method = localStorage.getItem('method') || 'fast';

    const params = new URLSearchParams();
    selectedGenres.forEach(genre => params.append('genres', genre));
    params.append('method', method);

    fetch(`http://localhost:5000/get_recommendations?${params.toString()}`)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            const movies = data.movies;
            if (!movies || movies.length === 0) {
                document.querySelector('header .results-box').innerHTML +=
                    '<p>No movies found matching your criteria.</p>';
                return;
            }

            for (let i = 0; i < Math.min(movies.length, 3); i++) {
                const movie = movies[i];

                const allBoxes = document.querySelectorAll('.results-box');
                const resultBox = allBoxes[i + 1]; 

                if (!resultBox) {
                    console.warn(`resultBox ${i + 1} not found`);
                    continue;
                }

                const titleElement = resultBox.querySelector('h2');
                if (titleElement) titleElement.textContent = movie.title;

                const ratingElement = resultBox.querySelector('.rating');
                if (ratingElement) ratingElement.textContent = movie.rating;

                const genresElement = resultBox.querySelector('.genres');
                if (genresElement) genresElement.textContent = Array.isArray(movie.genres) ? movie.genres.join(', ') : movie.genres;

                const posterElement = resultBox.querySelector('.poster');
                if (posterElement && movie.posterUrl) {
                    posterElement.src = movie.posterUrl;
                }

            }
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            document.querySelector('header .results-box').innerHTML +=
                '<p>Error loading movie recommendations. Please try again.</p>';
        });
});
