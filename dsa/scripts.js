document.getElementById('Done').addEventListener('click', function() {
    const selectedGenres = [];
    const genres = document.querySelectorAll('input[name="genre"]:checked');

    genres.forEach(genre => {
        selectedGenres.push(genre.value.toLowerCase()); 
    });
    localStorage.setItem('selectedGenres', JSON.stringify(selectedGenres));
    const methodElement = document.querySelector('input[name="speed"]:checked');
    const method = methodElement ? methodElement.value : 'fast';
    localStorage.setItem('method', method);
    window.location.href = 'movie results.html';
});
