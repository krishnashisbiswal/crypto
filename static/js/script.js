// ===== DOM ELEMENTS =====
const navbar = document.querySelector('.navbar');
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const investBtn = document.getElementById('investBtn');
const demoBtn = document.getElementById('demoBtn');
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');
const showSignupLink = document.getElementById('showSignup');
const showLoginLink = document.getElementById('showLogin');
const closeBtns = document.querySelectorAll('.close');
const faqItems = document.querySelectorAll('.faq-item');
const newsletterForm = document.querySelector('.newsletter-form');

// ===== NAVBAR SCROLL EFFECT =====
window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navbar.style.background = 'rgba(15, 23, 42, 0.98)';
        navbar.style.boxShadow = '0 4px 6px -1px rgb(0 0 0 / 0.1)';
    } else {
        navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// ===== MOBILE MENU TOGGLE =====
hamburger?.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// ===== LIVE PRICE UPDATES =====
function updateLivePrice() {
    const priceElement = document.getElementById('livePrice');
    const changeElement = document.getElementById('priceChange');
    
    if (priceElement && changeElement) {
        // Simulate price changes
        const basePrice = 89.45;
        const variation = (Math.random() - 0.5) * 2; // ±1
        const newPrice = basePrice + variation;
        const change = variation;
        const changePercent = (change / basePrice * 100);
        
        priceElement.textContent = `${newPrice.toFixed(2)}`;
        changeElement.textContent = `${change >= 0 ? '+' : ''}${change.toFixed(2)} (${change >= 0 ? '+' : ''}${changePercent.toFixed(2)}%)`;
        changeElement.className = `price-change ${change >= 0 ? 'positive' : 'negative'}`;
    }
}

// ===== LIVE TIME UPDATE =====
function updateCurrentTime() {
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour12: false,
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timeElement.textContent = timeString;
    }
}

// ===== HERO CHART =====
function initHeroChart() {
    const canvas = document.getElementById('heroChart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width;
    const height = canvas.height;
    
    // Generate sample data
    const dataPoints = 50;
    const data = [];
    let basePrice = 85;
    
    for (let i = 0; i < dataPoints; i++) {
        basePrice += (Math.random() - 0.5) * 2;
        data.push(basePrice);
    }
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    // Set up gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, height);
    gradient.addColorStop(0, 'rgba(34, 197, 94, 0.3)');
    gradient.addColorStop(1, 'rgba(34, 197, 94, 0.05)');
    
    // Draw area chart
    ctx.beginPath();
    const stepX = width / (dataPoints - 1);
    const minPrice = Math.min(...data);
    const maxPrice = Math.max(...data);
    const priceRange = maxPrice - minPrice;
    
    for (let i = 0; i < dataPoints; i++) {
        const x = i * stepX;
        const y = height - ((data[i] - minPrice) / priceRange) * (height - 20) - 10;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    
    // Complete the area
    ctx.lineTo(width, height);
    ctx.lineTo(0, height);
    ctx.closePath();
    
    // Fill area
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw line
    ctx.beginPath();
    for (let i = 0; i < dataPoints; i++) {
        const x = i * stepX;
        const y = height - ((data[i] - minPrice) / priceRange) * (height - 20) - 10;
        
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.strokeStyle = '#22c55e';
    ctx.lineWidth = 2;
    ctx.stroke();
}

// ===== MARKET DATA UPDATES =====
function updateMarketData() {
    const marketData = {
        goldPrice: { element: 'goldPrice', base: 2023.45, variation: 10 },
        oilPrice: { element: 'oilPrice', base: 89.23, variation: 2 },
        usdInr: { element: 'usdInr', base: 83.45, variation: 0.5 },
        btcPrice: { element: 'btcPrice', base: 97000, variation: 1000 },
        nasdaq: { element: 'nasdaq', base: 15234.67, variation: 100 }
    };
    
    Object.values(marketData).forEach(({ element, base, variation }) => {
        const el = document.getElementById(element);
        if (el) {
            const change = (Math.random() - 0.5) * variation * 2;
            const newValue = base + change;
            
            if (element === 'usdInr') {
                el.textContent = `₹${newValue.toFixed(2)}`;
            } else if (element === 'btcPrice') {
                el.textContent = `${Math.round(newValue).toLocaleString()}`;
            } else if (element === 'nasdaq') {
                el.textContent = newValue.toFixed(2);
            } else {
                el.textContent = `${newValue.toFixed(2)}`;
            }
        }
    });
}

// ===== SMOOTH SCROLLING =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== MODAL FUNCTIONALITY =====
function openModal(modal) {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal(modal) {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Invest button opens signup modal
investBtn?.addEventListener('click', () => {
    openModal(signupModal);
});

// Demo button functionality
demoBtn?.addEventListener('click', () => {
    alert('Demo functionality will be available soon!');
});

// Show signup modal
showSignupLink?.addEventListener('click', (e) => {
    e.preventDefault();
    closeModal(loginModal);
    openModal(signupModal);
});

// Show login modal
showLoginLink?.addEventListener('click', (e) => {
    e.preventDefault();
    closeModal(signupModal);
    openModal(loginModal);
});

// Close modal buttons
closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        closeModal(loginModal);
        closeModal(signupModal);
    });
});

// Close modal on outside click
window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        closeModal(loginModal);
    }
    if (e.target === signupModal) {
        closeModal(signupModal);
    }
});

// ===== FAQ FUNCTIONALITY =====
faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
        const isActive = item.classList.contains('active');
        
        // Close all FAQ items
        faqItems.forEach(faq => faq.classList.remove('active'));
        
        // Open clicked item if it wasn't active
        if (!isActive) {
            item.classList.add('active');
        }
    });
});

// ===== NEWSLETTER FORM =====
newsletterForm?.addEventListener('submit', (e) => {
    e.preventDefault();
    const email = e.target.querySelector('input[type="email"]').value;
    if (email) {
        alert('Thank you for subscribing! We\'ll keep you updated.');
        e.target.reset();
    }
});

// ===== TRADING INTERFACE INTERACTIONS =====
document.querySelectorAll('.trade-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const action = btn.classList.contains('buy-btn') ? 'BUY' : 'SELL';
        alert(`${action} order simulation - Demo mode active!`);
    });
});

// ===== ANIMATIONS ON SCROLL =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.querySelectorAll('.feature-card, .testimonial-card, .step-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
    // Initialize hero chart
    initHeroChart();
    
    // Start live updates
    updateCurrentTime();
    updateLivePrice();
    updateMarketData();
    
    // Set up intervals for live updates
    setInterval(updateCurrentTime, 1000);
    setInterval(updateLivePrice, 5000);
    setInterval(updateMarketData, 10000);
    setInterval(initHeroChart, 30000); // Refresh chart every 30 seconds
    
    // Add loading animation end
    document.body.classList.add('loaded');
});

// ===== KEYBOARD NAVIGATION =====
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal(loginModal);
        closeModal(signupModal);
    }
});

// ===== PERFORMANCE OPTIMIZATION =====
// Throttle scroll events
let ticking = false;
function updateOnScroll() {
    // Update navbar opacity based on scroll
    const scrolled = window.scrollY;
    const rate = scrolled * -0.5;
    
    // Parallax effect for hero elements
    const heroElements = document.querySelectorAll('.floating-card, .orb');
    heroElements.forEach((el, index) => {
        if (el) {
            el.style.transform = `translateY(${rate * (index + 1) * 0.1}px)`;
        }
    });
    
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateOnScroll);
        ticking = true;
    }
});

// ===== ERROR HANDLING =====
window.addEventListener('error', (e) => {
    console.error('An error occurred:', e.error);
});

// ===== RESPONSIVE CHART HANDLING =====
window.addEventListener('resize', () => {
    setTimeout(initHeroChart, 100);
});