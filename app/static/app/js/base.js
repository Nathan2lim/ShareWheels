// Script principal pour l'ensemble du site SherWheels

document.addEventListener('DOMContentLoaded', function() {
    // Gestion des messages existants (code original)
    initMessages();
    
    // Ajout de classes pour styliser les éléments Bootstrap
    styleBootstrapElements();
    
    // Ajout des effets de scroll pour animer les éléments lors du défilement
    initScrollEffects();
    
    // Initialisation des tooltips et popovers Bootstrap
    initBootstrapComponents();
});

// Gestion des messages originale
function initMessages() {
    // Sélectionne tous les éléments de message
    const messages = document.querySelectorAll('.message');

    messages.forEach((message) => {
        // Ajoute un gestionnaire d'événement pour cacher le message au clic
        message.addEventListener('click', () => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0'; // Ajoute une transition pour un effet fluide
            setTimeout(() => message.remove(), 500); // Supprime l'élément après la transition
        });

        // Cache automatiquement le message après 15 secondes
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease';
            message.style.opacity = '0'; // Transition fluide
            setTimeout(() => message.remove(), 500); // Supprime l'élément après la transition
        }, 15000);
    });
    
    // Nouvelle gestion pour les messages flash de Django
    const flashMessages = document.querySelectorAll('.messages-container li');
    
    flashMessages.forEach(message => {
        // Ajout d'un bouton de fermeture
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'close-message';
        closeBtn.onclick = function() {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        };
        
        message.appendChild(closeBtn);
        
        // Auto-fermeture après 5 secondes pour les messages de succès
        if (message.classList.contains('success')) {
            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            }, 5000);
        }
    });
}

// Applique nos styles personnalisés aux éléments Bootstrap
function styleBootstrapElements() {
    // Styliser les boutons
    document.querySelectorAll('.btn').forEach(btn => {
        if (!btn.classList.contains('btn-link') && 
            !btn.classList.contains('navbar-toggler') && 
            !btn.classList.contains('close')) {
            
            // Ajouter classe de transition si elle n'existe pas déjà
            if (!btn.style.transition) {
                btn.style.transition = 'all 0.3s';
            }
        }
    });
    
    // Styliser les tableaux
    document.querySelectorAll('table:not(.no-style)').forEach(table => {
        if (!table.classList.contains('table')) {
            table.classList.add('table');
        }
    });
}

// Initialise les effets de défilement
function initScrollEffects() {
    // Animation au défilement pour les sections
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-on-scroll');
        elements.forEach((element, index) => {
            const elementPosition = element.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            
            if (elementPosition < screenPosition) {
                // Animation delay staggered for grid items
                const delay = element.closest('.gallery-grid, .tickets-table') ? 
                    index * 0.1 : 0;
                
                element.style.animationDelay = delay + 's';
                element.classList.add('visible');
                element.style.opacity = '1';
            }
        });
    };
    
    // Exécuter au chargement et au défilement
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// Initialise les composants Bootstrap qui nécessitent JavaScript
function initBootstrapComponents() {
    // Initialiser les tooltips Bootstrap si la fonction existe
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Initialiser les popovers Bootstrap si la fonction existe
    if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function (popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
}