/**
 * Sistema de Predicción IA - JavaScript Principal
 * Funcionalidades comunes para todas las páginas
 */

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap si existen
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Inicializar popovers de Bootstrap si existen
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }

    // Añadir clase 'active' al enlace de navegación actual
    highlightCurrentNavLink();

    // Añadir efectos de animación a las tarjetas
    animateCardsOnScroll();

    // Inicializar manejadores de formularios
    initFormHandlers();
});

/**
 * Resalta el enlace de navegación correspondiente a la página actual
 */
function highlightCurrentNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

/**
 * Añade animaciones a las tarjetas cuando aparecen en el viewport
 */
function animateCardsOnScroll() {
    const cards = document.querySelectorAll('.card');
    
    // Si IntersectionObserver está disponible, usarlo para animaciones al hacer scroll
    if ('IntersectionObserver' in window) {
        const cardObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate__animated', 'animate__fadeInUp');
                    cardObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        cards.forEach(card => {
            cardObserver.observe(card);
        });
    } else {
        // Fallback para navegadores que no soportan IntersectionObserver
        cards.forEach(card => {
            card.classList.add('animate__animated', 'animate__fadeIn');
        });
    }
}

/**
 * Inicializa manejadores para formularios comunes
 */
function initFormHandlers() {
    // Validación de formularios con clase 'needs-validation'
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
}

/**
 * Formatea un número como moneda (USD por defecto)
 * @param {number} amount - Cantidad a formatear
 * @param {string} locale - Configuración regional (por defecto 'es-ES')
 * @param {string} currency - Moneda (por defecto 'USD')
 * @returns {string} Cantidad formateada como moneda
 */
function formatCurrency(amount, locale = 'es-ES', currency = 'USD') {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Muestra un mensaje de notificación
 * @param {string} message - Mensaje a mostrar
 * @param {string} type - Tipo de mensaje (success, error, warning, info)
 * @param {number} duration - Duración en milisegundos
 */
function showNotification(message, type = 'info', duration = 3000) {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getIconForType(type)}"></i>
            <span>${message}</span>
        </div>
    `;
    
    // Añadir al DOM
    document.body.appendChild(notification);
    
    // Mostrar con animación
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Ocultar después de la duración especificada
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, duration);
}

/**
 * Obtiene el icono correspondiente al tipo de notificación
 * @param {string} type - Tipo de notificación
 * @returns {string} Nombre del icono de Font Awesome
 */
function getIconForType(type) {
    switch (type) {
        case 'success':
            return 'check-circle';
        case 'error':
            return 'exclamation-circle';
        case 'warning':
            return 'exclamation-triangle';
        case 'info':
        default:
            return 'info-circle';
    }
}

/**
 * Crea un gráfico de líneas para mostrar datos históricos
 * @param {string} elementId - ID del elemento canvas
 * @param {Array} labels - Etiquetas para el eje X
 * @param {Array} datasets - Conjuntos de datos para el gráfico
 * @param {Object} options - Opciones adicionales para el gráfico
 * @returns {Object} Instancia del gráfico creado
 */
function createLineChart(elementId, labels, datasets, options = {}) {
    const ctx = document.getElementById(elementId).getContext('2d');
    
    // Opciones por defecto
    const defaultOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom'
            },
            tooltip: {
                mode: 'index',
                intersect: false
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.05)'
                }
            }
        }
    };
    
    // Combinar opciones por defecto con las proporcionadas
    const chartOptions = { ...defaultOptions, ...options };
    
    // Crear y devolver el gráfico
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: chartOptions
    });
}