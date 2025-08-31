// Dex Volkov - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize video players
    initVideoPlayers();
    
    // Smooth scrolling for navigation
    initSmoothScroll();
    
    // Alert close buttons
    initAlerts();
    
    // Video modal functionality
    initVideoModal();
    
    // Parallax effects
    initParallax();
    
    // Navbar scroll effects
    initNavbarScroll();
});

function initVideoPlayers() {
    // Initialize Plyr for all video elements
    const players = Array.from(document.querySelectorAll('video')).map(video => {
        return new Plyr(video, {
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'fullscreen'],
            hideControls: true,
            resetOnEnd: true,
            keyboard: { focused: true, global: false },
            tooltips: { controls: false, seek: true },
            settings: [],
            ratio: '16:9'
        });
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80; // Navbar height
                const targetPosition = target.offsetTop - offset;
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initAlerts() {
    document.querySelectorAll('.alert-close').forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
}

function initVideoModal() {
    const modal = document.getElementById('video-modal');
    const modalPlayer = document.getElementById('modal-player');
    const modalClose = document.querySelector('.modal-close');
    
    // Open modal when video card is clicked
    document.querySelectorAll('.video-card').forEach(card => {
        card.addEventListener('click', function() {
            const videoId = this.dataset.videoId;
            // In production, fetch video URL from API
            // For now, use placeholder
            modal.style.display = 'flex';
            // modalPlayer.src = `/api/video/${videoId}`;
        });
    });
    
    // Close modal
    if (modalClose) {
        modalClose.addEventListener('click', function() {
            modal.style.display = 'none';
            modalPlayer.pause();
            modalPlayer.src = '';
        });
    }
    
    // Close modal when clicking outside
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            modalPlayer.pause();
            modalPlayer.src = '';
        }
    });
}

function initParallax() {
    const parallaxElements = document.querySelectorAll('.hero');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Add background on scroll
        if (currentScroll > 50) {
            navbar.style.background = 'rgba(10, 10, 10, 0.98)';
            navbar.style.backdropFilter = 'blur(15px)';
        } else {
            navbar.style.background = 'rgba(10, 10, 10, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
        }
        
        // Hide/show navbar on scroll
        if (currentScroll > lastScroll && currentScroll > 500) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScroll = currentScroll;
    });
}

// Typewriter effect for hero headline
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Initialize typewriter on hero headline
const heroHeadline = document.querySelector('.hero h1');
if (heroHeadline) {
    const originalText = heroHeadline.innerText;
    setTimeout(() => {
        typeWriter(heroHeadline, originalText, 30);
    }, 500);
}

// Add glitch effect to logo on hover
const logo = document.querySelector('.navbar-brand');
if (logo) {
    logo.addEventListener('mouseenter', function() {
        this.style.animation = 'glitch 0.3s ease';
        setTimeout(() => {
            this.style.animation = '';
        }, 300);
    });
}

// CSS for glitch animation
const style = document.createElement('style');
style.textContent = `
@keyframes glitch {
    0%, 100% { text-shadow: 0 0 5px var(--accent); }
    20% { text-shadow: 3px 0 5px var(--accent), -3px 0 5px var(--error); }
    40% { text-shadow: -3px 0 5px var(--accent), 3px 0 5px var(--success); }
    60% { text-shadow: 0 3px 5px var(--accent), 0 -3px 5px var(--warning); }
    80% { text-shadow: 0 0 10px var(--accent); }
}

@keyframes fadeOut {
    from { opacity: 1; transform: translateY(0); }
    to { opacity: 0; transform: translateY(-20px); }
}

.video-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.95);
    z-index: 10000;
    align-items: center;
    justify-content: center;
}

.modal-content {
    position: relative;
    width: 90%;
    max-width: 1200px;
}

.modal-close {
    position: absolute;
    top: -40px;
    right: 0;
    color: white;
    font-size: 2rem;
    cursor: pointer;
    transition: all 0.3s ease;
}

.modal-close:hover {
    color: var(--accent);
    transform: rotate(90deg);
}
`;
document.head.appendChild(style);