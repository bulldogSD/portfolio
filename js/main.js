// === MENU HAMBURGUER ===
const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navLinks.classList.toggle('open');
});

// Fecha o menu ao clicar em um link
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        menuToggle.classList.remove('active');
        navLinks.classList.remove('open');
    });
});

// === NAVBAR SCROLL EFFECT ===
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// === ANIMAÇÕES DE SCROLL ===
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
        if (entry.isIntersecting) {
            const delay = entry.target.classList.contains('projeto-card')
                ? index * 80
                : 0;

            setTimeout(() => {
                entry.target.classList.add('visible');
            }, delay);

            observer.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
});

document.querySelectorAll('.animate-on-scroll').forEach(el => {
    observer.observe(el);
});

// === FILTRO DE PROJETOS ===
const filtroBtns = document.querySelectorAll('.filtro-btn');
const cards = document.querySelectorAll('.projeto-card');

filtroBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filtroBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filtro = btn.dataset.filtro;

        cards.forEach(card => {
            const categoria = card.dataset.categoria;

            if (filtro === 'todos' || categoria === filtro) {
                card.classList.remove('hidden');
            } else {
                card.classList.add('hidden');
            }
        });
    });
});

// === TOGGLE TEMA CLARO/ESCURO ===
const themeToggle = document.querySelector('.theme-toggle');

const temaSalvo = localStorage.getItem('tema');
if (temaSalvo === 'claro') {
    document.body.classList.add('tema-claro');
    themeToggle.textContent = '☀️';
}

themeToggle.addEventListener('click', () => {
    document.body.classList.toggle('tema-claro');

    const isClaro = document.body.classList.contains('tema-claro');
    themeToggle.textContent = isClaro ? '☀️' : '🌙';

    localStorage.setItem('tema', isClaro ? 'claro' : 'escuro');
});

// === VALIDAÇÃO DO FORMULÁRIO ===
const form = document.getElementById('form-contato');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    const nome = document.getElementById('nome');
    const email = document.getElementById('email');
    const mensagem = document.getElementById('mensagem');
    let valido = true;

    // Limpa erros anteriores
    document.querySelectorAll('.form-erro').forEach(el => el.textContent = '');
    document.querySelectorAll('.erro').forEach(el => el.classList.remove('erro'));

    if (nome.value.trim().length < 2) {
        mostrarErro(nome, 'Nome deve ter pelo menos 2 caracteres.');
        valido = false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email.value)) {
        mostrarErro(email, 'Digite um email válido.');
        valido = false;
    }

    if (mensagem.value.trim().length < 10) {
        mostrarErro(mensagem, 'Mensagem deve ter pelo menos 10 caracteres.');
        valido = false;
    }

    if (valido) {
        const sucesso = document.querySelector('.form-sucesso');
        sucesso.style.display = 'block';
        form.reset();

        setTimeout(() => {
            sucesso.style.display = 'none';
        }, 4000);
    }
});

function mostrarErro(input, mensagem) {
    input.classList.add('erro');
    const erroSpan = input.parentElement.querySelector('.form-erro');
    erroSpan.textContent = mensagem;
}

// === LINK ATIVO NA NAVBAR ===
const sections = document.querySelectorAll('section[id]');

window.addEventListener('scroll', () => {
    const scrollY = window.scrollY + 120;

    sections.forEach(section => {
        const top = section.offsetTop;
        const height = section.offsetHeight;
        const id = section.getAttribute('id');
        const link = document.querySelector(`.nav-links a[href="#${id}"]`);

        if (link) {
            if (scrollY >= top && scrollY < top + height) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        }
    });
});
