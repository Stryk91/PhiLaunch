// PhiVector Main JavaScript
// Interactive functionality with φ-based timing

(function() {
    'use strict';

    // Constants (Fibonacci timing)
    const TIMING = {
        INSTANT: 89,
        FAST: 144,
        NORMAL: 233,
        SLOW: 377,
        LAZY: 610
    };

    // Smooth scroll for anchor links
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }

    // Fade-in animation on scroll
    function initScrollAnimations() {
        const observerOptions = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe cards and sections
        document.querySelectorAll('.card, .stat, .hero-content').forEach(el => {
            observer.observe(el);
        });
    }

    // Header scroll effect
    function initHeaderScroll() {
        const header = document.querySelector('.header');
        if (!header) return;

        let lastScroll = 0;

        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;

            if (currentScroll > 100) {
                header.style.boxShadow = '0 5px 13px rgba(0, 0, 0, 0.5)';
            } else {
                header.style.boxShadow = 'none';
            }

            lastScroll = currentScroll;
        });
    }

    // Stats counter animation
    function animateCounter(element, target, duration) {
        let current = 0;
        const increment = target / (duration / 16); // 60fps
        const isDecimal = target.toString().includes('.');

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = isDecimal ? current.toFixed(3) : Math.floor(current);
            }
        }, 16);
    }

    function initStatsCounters() {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const statValue = entry.target.querySelector('.stat-value');
                    if (statValue && !statValue.dataset.animated) {
                        const value = statValue.textContent.trim();

                        // Handle special cases
                        if (value === 'φ') {
                            statValue.textContent = '0.000';
                            setTimeout(() => {
                                animateCounter(statValue, 1.618, TIMING.LAZY);
                            }, TIMING.FAST);
                        } else if (value.includes('+')) {
                            const num = parseInt(value);
                            statValue.textContent = '0';
                            setTimeout(() => {
                                animateCounter(statValue, num, TIMING.SLOW);
                                setTimeout(() => {
                                    statValue.textContent = value;
                                }, TIMING.SLOW);
                            }, TIMING.FAST);
                        } else if (value.includes('%')) {
                            const num = parseInt(value);
                            statValue.textContent = '0%';
                            setTimeout(() => {
                                let current = 0;
                                const timer = setInterval(() => {
                                    current += 2;
                                    if (current >= num) {
                                        statValue.textContent = value;
                                        clearInterval(timer);
                                    } else {
                                        statValue.textContent = current + '%';
                                    }
                                }, 16);
                            }, TIMING.FAST);
                        }

                        statValue.dataset.animated = 'true';
                    }
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.stat').forEach(stat => {
            statsObserver.observe(stat);
        });
    }

    // Glow effect on hover for cards
    function initCardGlowEffects() {
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transition = `all ${TIMING.NORMAL}ms cubic-bezier(0.618, 0, 0.382, 1)`;
            });

            card.addEventListener('mouseleave', function() {
                this.style.transition = `all ${TIMING.NORMAL}ms cubic-bezier(0.618, 0, 0.382, 1)`;
            });
        });
    }

    // Button ripple effect (industrial style)
    function initButtonEffects() {
        document.querySelectorAll('.btn').forEach(button => {
            button.addEventListener('click', function(e) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const ripple = document.createElement('span');
                ripple.style.position = 'absolute';
                ripple.style.left = x + 'px';
                ripple.style.top = y + 'px';
                ripple.style.width = '0';
                ripple.style.height = '0';
                ripple.style.borderRadius = '50%';
                ripple.style.background = 'rgba(255, 255, 255, 0.5)';
                ripple.style.transform = 'translate(-50%, -50%)';
                ripple.style.pointerEvents = 'none';

                const existingRipple = this.querySelector('span');
                if (existingRipple) {
                    existingRipple.remove();
                }

                this.style.position = 'relative';
                this.style.overflow = 'hidden';
                this.appendChild(ripple);

                setTimeout(() => {
                    ripple.style.transition = `all ${TIMING.SLOW}ms cubic-bezier(0.618, 0, 0.382, 1)`;
                    ripple.style.width = '233px';
                    ripple.style.height = '233px';
                    ripple.style.opacity = '0';
                }, 10);

                setTimeout(() => {
                    ripple.remove();
                }, TIMING.SLOW + 100);
            });
        });
    }

    // Code block copy functionality
    function initCodeCopy() {
        document.querySelectorAll('pre').forEach(pre => {
            const button = document.createElement('button');
            button.textContent = 'Copy';
            button.style.position = 'absolute';
            button.style.top = '8px';
            button.style.right = '8px';
            button.style.padding = '5px 13px';
            button.style.background = 'var(--gunmetal)';
            button.style.color = 'var(--text-primary)';
            button.style.border = '1px solid var(--border-subtle)';
            button.style.borderRadius = 'var(--radius-3)';
            button.style.cursor = 'pointer';
            button.style.fontSize = 'var(--font-13)';
            button.style.fontFamily = 'var(--font-mono)';

            pre.style.position = 'relative';
            pre.appendChild(button);

            button.addEventListener('click', async () => {
                const code = pre.textContent.replace('Copy', '').trim();
                try {
                    await navigator.clipboard.writeText(code);
                    button.textContent = 'Copied!';
                    button.style.background = 'var(--fel-green)';
                    button.style.color = 'var(--black-pure)';

                    setTimeout(() => {
                        button.textContent = 'Copy';
                        button.style.background = 'var(--gunmetal)';
                        button.style.color = 'var(--text-primary)';
                    }, TIMING.LAZY * 3);
                } catch (err) {
                    button.textContent = 'Failed';
                    setTimeout(() => {
                        button.textContent = 'Copy';
                    }, TIMING.SLOW);
                }
            });
        });
    }

    // Active nav link highlighting
    function initActiveNav() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.nav-link');

        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#' + current) {
                    link.classList.add('active');
                    link.style.color = 'var(--text-accent)';
                    link.style.borderColor = 'var(--border-accent)';
                }
            });
        });
    }

    // Initialize all functionality
    function init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Initialize features
        initSmoothScroll();
        initScrollAnimations();
        initHeaderScroll();
        initStatsCounters();
        initCardGlowEffects();
        initButtonEffects();
        initCodeCopy();
        initActiveNav();

        // Log initialization (can be removed in production)
        console.log('%cPhiVector initialized', 'color: #00F0FF; font-size: 13px; font-weight: bold;');
        console.log('%cφ = 1.618', 'color: #5FBF00; font-size: 13px;');
    }

    // Start initialization
    init();

})();
