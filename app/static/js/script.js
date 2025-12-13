document.addEventListener('DOMContentLoaded', function() {
    const animateElements = document.querySelectorAll('.btn, .metric, .schulte-cell');
    
    animateElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 25);
    });
});