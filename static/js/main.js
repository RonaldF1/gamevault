document.addEventListener('DOMContentLoaded', () => {
    const inputBuscador = document.getElementById('buscador');
    
    if (inputBuscador) {
        inputBuscador.addEventListener('input', (e) => {
            const textoBusqueda = e.target.value.toLowerCase().trim();
            // Selecciona todas las columnas que contienen tarjetas de juegos
            const tarjetas = document.querySelectorAll('.col-juego');
            
            tarjetas.forEach(tarjeta => {
                // Buscamos el título dentro de esta tarjeta específica
                const titulo = tarjeta.querySelector('.card-title').textContent.toLowerCase();
                
                if (titulo.includes(textoBusqueda)) {
                    tarjeta.style.display = ''; // Muestra la tarjeta si coincide
                } else {
                    tarjeta.style.display = 'none'; // La oculta si no coincide
                }
            });
        });
    }
});
