/**
 * 🎅 Secret Santa - Application JavaScript
 * Gère le "login", la révélation, et les Easter Eggs!
 */

// ============================================
// 📊 STATE
// ============================================

let assignmentsData = null;
let failedAttempts = 0;
let konamiProgress = 0;
const KONAMI_CODE = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];
const ADMIN_PASSWORD = 'perenoel2024';

// ============================================
// 🚀 INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadAssignments();
    initSnowflakes();
    initEventListeners();
    initKonamiCode();
    initMusicToggle();
    initSnowflakeClick();
});

/**
 * Charge le fichier JSON des assignations
 */
async function loadAssignments() {
    try {
        const response = await fetch('data/assignments.json');
        if (!response.ok) throw new Error('Fichier non trouvé');
        assignmentsData = await response.json();
        
        // Mettre à jour le budget affiché
        if (assignmentsData.event?.budget) {
            document.getElementById('budget-display').textContent = assignmentsData.event.budget;
        }
        
        console.log('🎄 Données chargées avec succès!');
    } catch (error) {
        console.error('❌ Erreur de chargement:', error);
        showError('Oups ! Le Père Noël a égaré les données... 🎅❓');
    }
}

// ============================================
// ❄️ SNOWFLAKES
// ============================================

function initSnowflakes() {
    const container = document.getElementById('snow-container');
    const snowflakes = ['❄', '❅', '❆', '✦', '✧', '⋆'];
    
    function createSnowflake() {
        const snowflake = document.createElement('div');
        snowflake.className = 'snowflake';
        snowflake.textContent = snowflakes[Math.floor(Math.random() * snowflakes.length)];
        snowflake.style.left = Math.random() * 100 + 'vw';
        snowflake.style.animationDuration = (Math.random() * 3 + 4) + 's';
        snowflake.style.fontSize = (Math.random() * 1 + 0.5) + 'rem';
        snowflake.style.opacity = Math.random() * 0.7 + 0.3;
        
        container.appendChild(snowflake);
        
        // Supprimer après l'animation
        setTimeout(() => {
            snowflake.remove();
        }, 7000);
    }
    
    // Créer des flocons régulièrement
    setInterval(createSnowflake, 200);
    
    // Créer quelques flocons initiaux
    for (let i = 0; i < 20; i++) {
        setTimeout(createSnowflake, i * 100);
    }
}

function initSnowflakeClick() {
    // Easter egg: click sur les flocons fait un son
    document.getElementById('snow-container').addEventListener('click', (e) => {
        if (e.target.classList.contains('snowflake')) {
            playDing();
            e.target.style.transform = 'scale(2) rotate(180deg)';
            setTimeout(() => e.target.remove(), 300);
        }
    });
}

function playDing() {
    // Créer un son simple avec l'API Web Audio
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.value = 800 + Math.random() * 400;
        oscillator.type = 'sine';
        
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    } catch (e) {
        // Audio non supporté, pas grave
    }
}

// ============================================
// 🎊 CONFETTI
// ============================================

function triggerConfetti() {
    const container = document.getElementById('confetti-container');
    const colors = ['#e63946', '#2a9d8f', '#f4a261', '#e9c46a', '#ffffff'];
    const shapes = ['■', '●', '▲', '★', '♦'];
    
    for (let i = 0; i < 100; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.textContent = shapes[Math.floor(Math.random() * shapes.length)];
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.color = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.fontSize = (Math.random() * 1.5 + 0.5) + 'rem';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            
            container.appendChild(confetti);
            
            setTimeout(() => confetti.remove(), 4000);
        }, i * 30);
    }
}

// ============================================
// 🔐 LOGIN LOGIC
// ============================================

function initEventListeners() {
    const loginForm = document.getElementById('login-form');
    const logoutBtn = document.getElementById('logout-btn');
    const adminLogoutBtn = document.getElementById('admin-logout-btn');
    
    loginForm.addEventListener('submit', handleLogin);
    logoutBtn.addEventListener('click', handleLogout);
    adminLogoutBtn.addEventListener('click', handleLogout);
}

function handleLogin(e) {
    e.preventDefault();
    
    const codename = document.getElementById('codename').value.trim();
    const password = document.getElementById('password').value.trim();
    
    // Easter egg: Admin mode
    if (codename.toLowerCase() === 'admin' && password === ADMIN_PASSWORD) {
        showAdminView();
        return;
    }
    
    if (!assignmentsData) {
        showError('Les données ne sont pas encore chargées... Patiente un peu ! 🎄');
        return;
    }
    
    // Chercher le participant
    const participant = assignmentsData.participants.find(
        p => p.codename.toLowerCase() === codename.toLowerCase() && p.password === password
    );
    
    if (participant) {
        showReveal(participant);
        failedAttempts = 0;
    } else {
        failedAttempts++;
        handleFailedAttempt();
    }
}

function handleFailedAttempt() {
    const errorMessages = [
        "Ho ho NO ! Ce n'est pas le bon code... 🎅❌",
        "Hmm, le Père Noël ne te reconnaît pas... 🤔",
        "Mauvais mot de passe ! Les lutins vérifient... 🔍",
        "Accès refusé ! As-tu bien vérifié tes identifiants ? 🔐",
        "Nope ! Essaie encore, petit lutin ! 🧝",
    ];
    
    let message = errorMessages[Math.floor(Math.random() * errorMessages.length)];
    
    // Easter egg: 5 tentatives ratées
    if (failedAttempts >= 5) {
        message = "🎅 Le Père Noël te surveille... 👀 (5 tentatives ratées!)";
    }
    
    showError(message);
}

function showError(message) {
    const errorEl = document.getElementById('error-message');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
    
    // Faire vibrer le formulaire
    const form = document.getElementById('login-form');
    form.style.animation = 'none';
    form.offsetHeight; // Trigger reflow
    form.style.animation = 'shake 0.5s ease-in-out';
}

function hideError() {
    document.getElementById('error-message').classList.add('hidden');
}

// ============================================
// 🎁 REVEAL
// ============================================

function showReveal(participant) {
    hideError();
    
    // Mettre à jour le contenu
    document.getElementById('agent-name').textContent = participant.realName;
    document.getElementById('fun-message').textContent = participant.funMessage;
    document.getElementById('giftee-name').textContent = participant.giftee;
    
    // Basculer les sections
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('reveal-section').classList.remove('hidden');
    
    // Lancer les confettis !
    triggerConfetti();
    
    // Et un deuxième salve après un délai
    setTimeout(triggerConfetti, 1000);
}

function handleLogout() {
    // Réinitialiser le formulaire
    document.getElementById('login-form').reset();
    
    // Basculer les sections
    document.getElementById('login-section').classList.remove('hidden');
    document.getElementById('reveal-section').classList.add('hidden');
    document.getElementById('admin-section').classList.add('hidden');
}

// ============================================
// 👑 ADMIN VIEW
// ============================================

function showAdminView() {
    if (!assignmentsData) return;
    
    const adminList = document.getElementById('admin-list');
    adminList.innerHTML = '';
    
    assignmentsData.participants.forEach(p => {
        const item = document.createElement('div');
        item.className = 'admin-item';
        item.innerHTML = `
            <span class="giver">${p.realName}</span>
            <span class="arrow">→</span>
            <span class="receiver">${p.giftee}</span>
        `;
        adminList.appendChild(item);
    });
    
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('admin-section').classList.remove('hidden');
}

// ============================================
// 🎮 KONAMI CODE
// ============================================

function initKonamiCode() {
    document.addEventListener('keydown', (e) => {
        if (e.code === KONAMI_CODE[konamiProgress]) {
            konamiProgress++;
            
            if (konamiProgress === KONAMI_CODE.length) {
                triggerSantaDance();
                konamiProgress = 0;
            }
        } else {
            konamiProgress = 0;
        }
    });
}

function triggerSantaDance() {
    const santaDance = document.getElementById('santa-dance');
    santaDance.classList.remove('hidden');
    
    // Ajouter des emojis dansants
    const emojis = ['🎅', '💃', '🕺', '🦌', '⭐', '🎄', '🎁'];
    santaDance.textContent = emojis.sort(() => Math.random() - 0.5).slice(0, 4).join('');
    
    triggerConfetti();
    
    setTimeout(() => {
        santaDance.classList.add('hidden');
    }, 5000);
}

// ============================================
// 🎵 MUSIC TOGGLE
// ============================================

function initMusicToggle() {
    const musicBtn = document.getElementById('music-toggle');
    const audio = document.getElementById('jingle');
    
    // 🎵 Auto-play on first user interaction (click anywhere)
    function startMusicOnFirstInteraction() {
        audio.play().then(() => {
            musicBtn.textContent = '🔊';
            musicBtn.classList.add('playing');
            console.log('🎵 Musique de Noël activée ! 🎄');
        }).catch(() => {
            console.log('🎵 Could not autoplay');
        });
        // Remove listeners after first interaction
        document.removeEventListener('click', startMusicOnFirstInteraction);
        document.removeEventListener('keydown', startMusicOnFirstInteraction);
    }
    
    document.addEventListener('click', startMusicOnFirstInteraction);
    document.addEventListener('keydown', startMusicOnFirstInteraction);
    
    // Toggle button still works normally
    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().catch(() => {
                console.log('🎵 Interaction utilisateur requise pour la musique');
            });
            musicBtn.textContent = '🔊';
            musicBtn.classList.add('playing');
        } else {
            audio.pause();
            musicBtn.textContent = '🔇';
            musicBtn.classList.remove('playing');
        }
    });
}
