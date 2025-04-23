document.addEventListener('DOMContentLoaded', function () {
    const selectedGenres = JSON.parse(localStorage.getItem('selectedGenres')) || [];
    const method = localStorage.getItem('method') || 'fast';

    const params = new URLSearchParams();
    selectedGenres.forEach(genre => params.append('genres', genre));
    params.append('method', method);

    const minRating = localStorage.getItem('minrating') || 0;
    const maxRating = localStorage.getItem('maxrating') || 10;
    if(minRating) params.append('minrating', minRating);
    if(maxRating) params.append('maxrating', maxRating);


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

            const resultsContainer = document.getElementById('resultsContainer');

            for (let i = 0; i < Math.min(movies.length, 3); i++) {
                const movie = movies[i];
            
                const movieBox = document.createElement('div');
                movieBox.classList.add('movie-container');
            
                movieBox.innerHTML = `
                    <div class="poster-container">
                        <img src="${movie.posterUrl || 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/450px-No_image_available.svg.png'}" alt="Movie Poster" class="poster"/>

                    </div>
                    <div class="movie-info">
                        <h2>${movie.title}</h2><br>
                        <p>Rating: <span class="rating">${movie.rating}</span></p>
                        <p>Genre: <span class="genres">${Array.isArray(movie.genres) ? movie.genres.join(', ') : movie.genres}</span></p>
                        <p>Plot: <span class="plot">${movie.plot}</span></p>
                    </div>
                `;
            
                resultsContainer.appendChild(movieBox);
            }
            console.log("Movie data:", data.movies);

        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
            document.querySelector('header .results-box').innerHTML +=
                '<p>Error loading movie recommendations. Please try again.</p>';
        });
});
