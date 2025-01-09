window.addEventListener("load", function() {
    const overlay = document.getElementById('overlay');
    const button = document.getElementById('get-started');
    const sliderContainer = document.querySelector('.slider-container');

    sliderContainer.classList.add('hidden');

    document.body.classList.add('no-scroll');

    button.addEventListener('click', function() {
        overlay.style.display = 'none';
        // Mostrar el slider
        sliderContainer.classList.remove('hidden');
        // Habilitar el scroll
        document.body.classList.remove('no-scroll');
    });
});