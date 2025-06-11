document.addEventListener('DOMContentLoaded', function() {
    // Validación de formulario en cliente
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Actualización en tiempo real del dashboard
    if (document.getElementById('dataTable')) {
        setTimeout(function() {
            location.reload();
        }, 60000);  // Recargar cada minuto
    }
});