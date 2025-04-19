document.getElementById('Done').addEventListener('click', function() {
    const selectedGenres = [];
    const genres = document.querySelectorAll('input[name="genre"]:checked');
    
    genres.forEach(genre => {
        selectedGenres.push(genre.value);
    });
    localStorage.setItem('selectedGenres', JSON.stringify(selectedGenres));
    window.location.href = 'movie results.html';
});