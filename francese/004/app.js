// Ultra-colorful and addictive French Future Simple Quiz Game
class FuturSimpleQuiz {
    constructor() {
        this.currentScreen = 'home';
        this.gameData = {
            totalXP: 0,
            totalAchievements: 0,
            bestStreak: 0,
            unlockedAchievements: []
        };
        
        this.gameState = {
            currentLevel: '',
            questions: [],
            currentQuestionIndex: 0,
            score: 0,
            streak: 0,
            maxStreak: 0,
            correctAnswers: 0,
            timer: null,
            timeLeft: 0,
            isAnswered: false,
            powerUps: {
                fiftyFifty: 3,
                timeFreeze: 2,
                doublePoints: 2
            },
            doublePointsActive: false,
            timeFrozen: false,
            fiftyFiftyUsed: false
        };

        this.questions = [
            {
                question: "Come si coniuga 'parler' (parlare) alla 1a persona singolare del futuro semplice?",
                options: ["je parlerai", "je parlerais", "je parle", "j'ai parlé"],
                correct: 0,
                level: "beginner"
            },
            {
                question: "Quale è la forma corretta per 'tu finirai' in francese?",
                options: ["tu finiras", "tu finirais", "tu finis", "tu as fini"],
                correct: 0,
                level: "beginner"
            },
            {
                question: "Come si dice 'noi andremo' in francese (futuro semplice)?",
                options: ["nous irons", "nous allons", "nous sommes allés", "nous irions"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Qual è il futuro di 'être' alla 3a persona plurale?",
                options: ["ils seront", "ils sont", "ils étaient", "ils seraient"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Come si coniuga 'avoir' al futuro, 2a persona singolare?",
                options: ["tu auras", "tu as", "tu avais", "tu aurais"],
                correct: 0,
                level: "beginner"
            },
            {
                question: "'Faire' al futuro, 1a persona plurale:",
                options: ["nous ferons", "nous faisons", "nous avons fait", "nous ferions"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Come si dice 'lei verrà' in francese?",
                options: ["elle viendra", "elle vient", "elle est venue", "elle viendrait"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Il futuro di 'savoir' alla 2a persona plurale è:",
                options: ["vous saurez", "vous savez", "vous saviez", "vous sauriez"],
                correct: 0,
                level: "expert"
            },
            {
                question: "Come si coniuga 'voir' al futuro, 3a persona singolare?",
                options: ["il verra", "il voit", "il voyait", "il verrait"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "'Pouvoir' al futuro, 1a persona singolare:",
                options: ["je pourrai", "je peux", "je pouvais", "je pourrais"],
                correct: 0,
                level: "expert"
            },
            {
                question: "Come si dice 'voi dovrete' in francese?",
                options: ["vous devrez", "vous devez", "vous deviez", "vous devriez"],
                correct: 0,
                level: "expert"
            },
            {
                question: "Il futuro di 'vouloir' alla 3a persona plurale è:",
                options: ["ils voudront", "ils veulent", "ils voulaient", "ils voudraient"],
                correct: 0,
                level: "expert"
            },
            {
                question: "'Mettre' al futuro, 1a persona plurale:",
                options: ["nous mettrons", "nous mettons", "nous avons mis", "nous mettrions"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Come si coniuga 'prendre' al futuro, 2a persona singolare?",
                options: ["tu prendras", "tu prends", "tu as pris", "tu prendrais"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "'Recevoir' al futuro, 3a persona singolare:",
                options: ["il recevra", "il reçoit", "il recevait", "il recevrait"],
                correct: 0,
                level: "expert"
            },
            {
                question: "Come si dice 'io dovrò' in francese?",
                options: ["je devrai", "je dois", "je devais", "je devrais"],
                correct: 0,
                level: "beginner"
            },
            {
                question: "Il futuro di 'tenir' alla 2a persona plurale è:",
                options: ["vous tiendrez", "vous tenez", "vous teniez", "vous tiendriez"],
                correct: 0,
                level: "expert"
            },
            {
                question: "'Aller' al futuro, 3a persona plurale:",
                options: ["ils iront", "ils vont", "ils sont allés", "ils iraient"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "Come si coniuga 'dire' al futuro, 1a persona singolare?",
                options: ["je dirai", "je dis", "j'ai dit", "je dirais"],
                correct: 0,
                level: "intermediate"
            },
            {
                question: "'Sortir' al futuro, 2a persona singolare:",
                options: ["tu sortiras", "tu sors", "tu es sorti(e)", "tu sortirais"],
                correct: 0,
                level: "beginner"
            }
        ];

        this.levels = {
            beginner: { name: "Principiante", questions: 5, timeLimit: 20, color: "#32cd32" },
            intermediate: { name: "Intermedio", questions: 8, timeLimit: 15, color: "#ffa500" },
            expert: { name: "Esperto", questions: 7, timeLimit: 12, color: "#ff6b6b" }
        };

        this.achievements = [
            { name: "Primo Passo", description: "Completa il tuo primo quiz", icon: "🎉", id: "firstQuiz" },
            { name: "In Serie!", description: "Ottieni una streak di 5", icon: "🔥", id: "streak5" },
            { name: "Perfetto!", description: "Quiz completato senza errori", icon: "💎", id: "perfect" },
            { name: "Velocista", description: "Completa un quiz in meno di 60 secondi", icon: "⚡", id: "speedy" },
            { name: "Esperto", description: "Supera un quiz esperto", icon: "🏆", id: "expertLevel" },
            { name: "Maestro Streak", description: "Raggiungi una streak di 10", icon: "👑", id: "streak10" }
        ];

        this.motivationalMessages = [
            "🌟 Fantastico!", "💪 Sei in fiamme!", "🚀 Incredibile!", "⚡ Velocissimo!",
            "🎯 Perfetto!", "🔥 Inarrestabile!", "💎 Brillante!", "🏆 Campione!"
        ];

        this.init();
    }

    init() {
        this.createParticles();
        this.bindEvents();
        this.updateStats();
    }

    createParticles() {
        const container = document.querySelector('.particles-container');
        for (let i = 0; i < 10; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            container.appendChild(particle);
        }
    }

    bindEvents() {
        // Level selection
        document.querySelectorAll('.level-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const level = e.currentTarget.dataset.level;
                this.startQuiz(level);
            });
        });

        // Power-ups
        document.querySelectorAll('.power-up-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const powerUp = e.currentTarget.dataset.powerup;
                this.usePowerUp(powerUp);
            });
        });

        // Navigation buttons
        document.getElementById('quitQuiz').addEventListener('click', () => this.showScreen('home'));
        document.getElementById('playAgain').addEventListener('click', () => this.startQuiz(this.gameState.currentLevel));
        document.getElementById('backToHome').addEventListener('click', () => this.showScreen('home'));
        
        // Achievements modal
        document.getElementById('showAchievements').addEventListener('click', () => this.showAchievements());
        document.getElementById('closeAchievements').addEventListener('click', () => this.hideAchievements());
    }

    showScreen(screen) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        document.querySelector(`.${screen}-screen`).classList.add('active');
        this.currentScreen = screen;
    }

    startQuiz(level) {
        this.gameState.currentLevel = level;
        const levelConfig = this.levels[level];
        
        // Filter questions by level and shuffle
        const levelQuestions = this.questions.filter(q => q.level === level);
        this.gameState.questions = this.shuffleArray([...levelQuestions]).slice(0, levelConfig.questions);
        
        // Reset game state
        this.gameState.currentQuestionIndex = 0;
        this.gameState.score = 0;
        this.gameState.streak = 0;
        this.gameState.maxStreak = 0;
        this.gameState.correctAnswers = 0;
        this.gameState.isAnswered = false;
        this.gameState.doublePointsActive = false;
        this.gameState.timeFrozen = false;
        this.gameState.fiftyFiftyUsed = false;
        
        // Reset power-ups
        this.gameState.powerUps = { fiftyFifty: 3, timeFreeze: 2, doublePoints: 2 };
        
        this.showScreen('quiz');
        this.displayQuestion();
        this.updateQuizUI();
        this.startTimer(levelConfig.timeLimit);
    }

    displayQuestion() {
        const question = this.gameState.questions[this.gameState.currentQuestionIndex];
        document.getElementById('questionText').textContent = question.question;
        
        const answersGrid = document.getElementById('answersGrid');
        answersGrid.innerHTML = '';
        
        question.options.forEach((option, index) => {
            const button = document.createElement('button');
            button.className = 'answer-btn';
            button.textContent = option;
            button.addEventListener('click', () => this.selectAnswer(index));
            answersGrid.appendChild(button);
        });
        
        this.gameState.isAnswered = false;
        this.gameState.fiftyFiftyUsed = false;
        this.updateProgress();
    }

    selectAnswer(selectedIndex) {
        if (this.gameState.isAnswered) return;
        
        this.gameState.isAnswered = true;
        clearInterval(this.gameState.timer);
        
        const question = this.gameState.questions[this.gameState.currentQuestionIndex];
        const isCorrect = selectedIndex === question.correct;
        const answerButtons = document.querySelectorAll('.answer-btn');
        
        // Disable all buttons
        answerButtons.forEach(btn => btn.classList.add('disabled'));
        
        // Show correct/incorrect feedback
        answerButtons[selectedIndex].classList.add(isCorrect ? 'correct' : 'incorrect');
        if (!isCorrect) {
            answerButtons[question.correct].classList.add('correct');
        }
        
        if (isCorrect) {
            this.handleCorrectAnswer();
        } else {
            this.handleIncorrectAnswer();
        }
        
        // Move to next question after delay
        setTimeout(() => {
            this.nextQuestion();
        }, 1500);
    }

    handleCorrectAnswer() {
        this.gameState.correctAnswers++;
        this.gameState.streak++;
        this.gameState.maxStreak = Math.max(this.gameState.maxStreak, this.gameState.streak);
        
        // Calculate score with multipliers
        let points = 100;
        if (this.gameState.streak >= 5) points *= 1.5;
        if (this.gameState.streak >= 10) points *= 2;
        if (this.gameState.doublePointsActive) {
            points *= 2;
            this.gameState.doublePointsActive = false;
        }
        
        this.gameState.score += Math.round(points);
        
        // Show motivational message
        this.showMotivationalMessage();
        
        // Particle effects
        this.createSuccessParticles();
        
        this.updateQuizUI();
    }

    handleIncorrectAnswer() {
        this.gameState.streak = 0;
        this.gameState.doublePointsActive = false;
        
        // Shake effect
        document.querySelector('.quiz-screen').style.animation = 'shake 0.6s ease';
        setTimeout(() => {
            document.querySelector('.quiz-screen').style.animation = '';
        }, 600);
    }

    nextQuestion() {
        this.gameState.currentQuestionIndex++;
        
        if (this.gameState.currentQuestionIndex >= this.gameState.questions.length) {
            this.endQuiz();
        } else {
            this.displayQuestion();
            const levelConfig = this.levels[this.gameState.currentLevel];
            this.startTimer(levelConfig.timeLimit);
        }
    }

    startTimer(seconds) {
        this.gameState.timeLeft = seconds;
        this.updateTimer();
        
        this.gameState.timer = setInterval(() => {
            if (!this.gameState.timeFrozen) {
                this.gameState.timeLeft--;
                this.updateTimer();
                
                if (this.gameState.timeLeft <= 0) {
                    this.timeUp();
                }
            }
        }, 1000);
    }

    updateTimer() {
        const timerText = document.getElementById('timerText');
        const timerCircle = document.getElementById('timerCircle');
        const levelConfig = this.levels[this.gameState.currentLevel];
        
        timerText.textContent = this.gameState.timeLeft;
        
        const progress = this.gameState.timeLeft / levelConfig.timeLimit;
        const dashOffset = 157 * (1 - progress);
        timerCircle.style.strokeDashoffset = dashOffset;
        
        // Change color based on time left
        if (this.gameState.timeLeft <= 5) {
            timerCircle.style.stroke = '#ff6b6b';
            timerText.style.color = '#ff6b6b';
        } else if (this.gameState.timeLeft <= 10) {
            timerCircle.style.stroke = '#ffa500';
            timerText.style.color = '#ffa500';
        }
    }

    timeUp() {
        if (this.gameState.isAnswered) return;
        
        this.gameState.isAnswered = true;
        clearInterval(this.gameState.timer);
        
        // Show correct answer
        const question = this.gameState.questions[this.gameState.currentQuestionIndex];
        const answerButtons = document.querySelectorAll('.answer-btn');
        answerButtons.forEach(btn => btn.classList.add('disabled'));
        answerButtons[question.correct].classList.add('correct');
        
        this.handleIncorrectAnswer();
        
        setTimeout(() => {
            this.nextQuestion();
        }, 1500);
    }

    usePowerUp(powerUp) {
        if (this.gameState.powerUps[powerUp] <= 0 || this.gameState.isAnswered) return;
        
        // Check if 50/50 is already used for this question
        if (powerUp === 'fiftyFifty' && this.gameState.fiftyFiftyUsed) return;
        
        this.gameState.powerUps[powerUp]--;
        this.updatePowerUpUI();
        
        switch (powerUp) {
            case 'fiftyFifty':
                this.fiftyFiftyPowerUp();
                break;
            case 'timeFreeze':
                this.timeFreezePowerUp();
                break;
            case 'doublePoints':
                this.doublePointsPowerUp();
                break;
        }
    }

    fiftyFiftyPowerUp() {
        const question = this.gameState.questions[this.gameState.currentQuestionIndex];
        const answerButtons = document.querySelectorAll('.answer-btn');
        const incorrectIndices = [];
        
        // Find all incorrect answer indices
        question.options.forEach((option, index) => {
            if (index !== question.correct) {
                incorrectIndices.push(index);
            }
        });
        
        // Remove 2 random incorrect answers
        const toRemove = this.shuffleArray([...incorrectIndices]).slice(0, 2);
        toRemove.forEach(index => {
            const button = answerButtons[index];
            button.style.opacity = '0.3';
            button.style.pointerEvents = 'none';
            button.style.transform = 'scale(0.9)';
            button.style.filter = 'blur(1px)';
            button.classList.add('disabled');
        });
        
        // Mark 50/50 as used for this question
        this.gameState.fiftyFiftyUsed = true;
        
        // Visual feedback for power-up activation
        const fiftyFiftyBtn = document.getElementById('fiftyFifty');
        fiftyFiftyBtn.style.animation = 'pulse 0.6s ease';
        setTimeout(() => {
            fiftyFiftyBtn.style.animation = '';
        }, 600);
    }

    timeFreezePowerUp() {
        this.gameState.timeFrozen = true;
        setTimeout(() => {
            this.gameState.timeFrozen = false;
        }, 10000);
        
        // Visual feedback
        const timerCircle = document.querySelector('.timer-circle');
        timerCircle.style.filter = 'hue-rotate(180deg)';
        timerCircle.style.animation = 'pulse 1s ease-in-out infinite';
        
        setTimeout(() => {
            timerCircle.style.filter = '';
            timerCircle.style.animation = '';
        }, 10000);
    }

    doublePointsPowerUp() {
        this.gameState.doublePointsActive = true;
        
        // Visual feedback
        const scoreElement = document.getElementById('currentScore');
        scoreElement.style.animation = 'pulse 1s ease-in-out 3';
        scoreElement.style.color = '#ffa500';
        
        setTimeout(() => {
            scoreElement.style.animation = '';
            scoreElement.style.color = '';
        }, 3000);
    }

    endQuiz() {
        clearInterval(this.gameState.timer);
        
        // Calculate XP and update stats
        const earnedXP = Math.round(this.gameState.score / 10);
        this.gameData.totalXP += earnedXP;
        this.gameData.bestStreak = Math.max(this.gameData.bestStreak, this.gameState.maxStreak);
        
        // Check for achievements
        const newAchievements = this.checkAchievements();
        
        this.showResults(earnedXP, newAchievements);
        this.updateStats();
    }

    showResults(earnedXP, newAchievements) {
        this.showScreen('results');
        
        // Set results data
        document.getElementById('finalScore').textContent = this.gameState.score.toLocaleString();
        document.getElementById('correctAnswers').textContent = `${this.gameState.correctAnswers}/${this.gameState.questions.length}`;
        document.getElementById('maxStreak').textContent = this.gameState.maxStreak;
        document.getElementById('earnedXP').textContent = earnedXP;
        
        // Set results title and emoji based on performance
        const percentage = (this.gameState.correctAnswers / this.gameState.questions.length) * 100;
        let title, emoji;
        
        if (percentage === 100) {
            title = "🎉 PERFETTO! 🎉";
            emoji = "👑";
        } else if (percentage >= 80) {
            title = "🌟 FANTASTICO! 🌟";
            emoji = "🎊";
        } else if (percentage >= 60) {
            title = "👍 BRAVO! 👍";
            emoji = "🎯";
        } else {
            title = "💪 Riprova! 💪";
            emoji = "🚀";
        }
        
        document.getElementById('resultsTitle').textContent = title;
        document.getElementById('resultsEmoji').textContent = emoji;
        
        // Show new achievements
        const achievementsContainer = document.getElementById('achievementsEarned');
        achievementsContainer.innerHTML = '';
        
        if (newAchievements.length > 0) {
            newAchievements.forEach(achievement => {
                const div = document.createElement('div');
                div.className = 'achievement-notification';
                div.innerHTML = `
                    <div>${achievement.icon} ${achievement.name}</div>
                    <div style="font-size: 0.9em; opacity: 0.9;">${achievement.description}</div>
                `;
                achievementsContainer.appendChild(div);
            });
        }
        
        // Confetti for good results
        if (percentage >= 80) {
            this.createConfetti();
        }
    }

    checkAchievements() {
        const newAchievements = [];
        
        // First quiz
        if (!this.gameData.unlockedAchievements.includes('firstQuiz')) {
            this.gameData.unlockedAchievements.push('firstQuiz');
            newAchievements.push(this.achievements.find(a => a.id === 'firstQuiz'));
        }
        
        // Streak achievements
        if (this.gameState.maxStreak >= 5 && !this.gameData.unlockedAchievements.includes('streak5')) {
            this.gameData.unlockedAchievements.push('streak5');
            newAchievements.push(this.achievements.find(a => a.id === 'streak5'));
        }
        
        if (this.gameState.maxStreak >= 10 && !this.gameData.unlockedAchievements.includes('streak10')) {
            this.gameData.unlockedAchievements.push('streak10');
            newAchievements.push(this.achievements.find(a => a.id === 'streak10'));
        }
        
        // Perfect quiz
        if (this.gameState.correctAnswers === this.gameState.questions.length && !this.gameData.unlockedAchievements.includes('perfect')) {
            this.gameData.unlockedAchievements.push('perfect');
            newAchievements.push(this.achievements.find(a => a.id === 'perfect'));
        }
        
        // Expert level
        if (this.gameState.currentLevel === 'expert' && this.gameState.correctAnswers >= 5 && !this.gameData.unlockedAchievements.includes('expertLevel')) {
            this.gameData.unlockedAchievements.push('expertLevel');
            newAchievements.push(this.achievements.find(a => a.id === 'expertLevel'));
        }
        
        this.gameData.totalAchievements = this.gameData.unlockedAchievements.length;
        
        return newAchievements;
    }

    showAchievements() {
        const modal = document.getElementById('achievementsModal');
        const grid = document.getElementById('achievementsGrid');
        
        grid.innerHTML = '';
        
        this.achievements.forEach(achievement => {
            const isUnlocked = this.gameData.unlockedAchievements.includes(achievement.id);
            const card = document.createElement('div');
            card.className = `achievement-card ${isUnlocked ? 'unlocked' : ''}`;
            
            card.innerHTML = `
                <div class="achievement-icon">${isUnlocked ? achievement.icon : '🔒'}</div>
                <div class="achievement-name">${achievement.name}</div>
                <div class="achievement-description">${achievement.description}</div>
            `;
            
            grid.appendChild(card);
        });
        
        modal.classList.remove('hidden');
    }

    hideAchievements() {
        document.getElementById('achievementsModal').classList.add('hidden');
    }

    updateQuizUI() {
        document.getElementById('currentScore').textContent = this.gameState.score.toLocaleString();
        document.getElementById('currentStreak').textContent = this.gameState.streak;
        document.getElementById('currentXP').textContent = this.gameData.totalXP;
        
        this.updatePowerUpUI();
    }

    updatePowerUpUI() {
        Object.keys(this.gameState.powerUps).forEach(powerUp => {
            const btn = document.getElementById(powerUp);
            const usesElement = btn.querySelector('.power-up-uses');
            usesElement.textContent = this.gameState.powerUps[powerUp];
            btn.disabled = this.gameState.powerUps[powerUp] <= 0;
            
            // Special handling for 50/50 if already used this question
            if (powerUp === 'fiftyFifty' && this.gameState.fiftyFiftyUsed) {
                btn.disabled = true;
                btn.style.opacity = '0.5';
            }
        });
    }

    updateProgress() {
        const progress = ((this.gameState.currentQuestionIndex) / this.gameState.questions.length) * 100;
        document.getElementById('progressFill').style.width = `${progress}%`;
        document.getElementById('currentQuestion').textContent = this.gameState.currentQuestionIndex + 1;
        document.getElementById('totalQuestions').textContent = this.gameState.questions.length;
    }

    updateStats() {
        document.getElementById('totalXP').textContent = this.gameData.totalXP;
        document.getElementById('totalAchievements').textContent = this.gameData.totalAchievements;
        document.getElementById('bestStreak').textContent = this.gameData.bestStreak;
    }

    showMotivationalMessage() {
        const message = this.getRandomMessage();
        const element = document.getElementById('motivationalMessage');
        element.textContent = message;
        element.classList.remove('hidden');
        
        setTimeout(() => {
            element.classList.add('hidden');
        }, 2000);
    }

    getRandomMessage() {
        return this.motivationalMessages[Math.floor(Math.random() * this.motivationalMessages.length)];
    }

    createSuccessParticles() {
        const container = document.querySelector('.particles-container');
        
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.position = 'absolute';
            particle.style.width = '6px';
            particle.style.height = '6px';
            particle.style.borderRadius = '50%';
            particle.style.backgroundColor = ['#ff6b6b', '#ffa500', '#ffff00', '#32cd32', '#00bfff', '#8a2be2'][Math.floor(Math.random() * 6)];
            particle.style.left = '50%';
            particle.style.top = '50%';
            particle.style.pointerEvents = 'none';
            particle.style.zIndex = '999';
            
            const angle = (Math.PI * 2 * i) / 20;
            const velocity = 100 + Math.random() * 100;
            const vx = Math.cos(angle) * velocity;
            const vy = Math.sin(angle) * velocity;
            
            container.appendChild(particle);
            
            let x = 0, y = 0, gravity = 500, time = 0;
            
            const animate = () => {
                time += 0.016;
                x = vx * time;
                y = vy * time + 0.5 * gravity * time * time;
                
                particle.style.transform = `translate(${x}px, ${y}px)`;
                particle.style.opacity = Math.max(0, 1 - time * 2);
                
                if (time < 1) {
                    requestAnimationFrame(animate);
                } else {
                    container.removeChild(particle);
                }
            };
            
            requestAnimationFrame(animate);
        }
    }

    createConfetti() {
        const container = document.querySelector('.confetti-container');
        
        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.animationDelay = Math.random() * 3 + 's';
            confetti.style.animationDuration = (Math.random() * 3 + 2) + 's';
            container.appendChild(confetti);
            
            setTimeout(() => {
                container.removeChild(confetti);
            }, 5000);
        }
    }

    shuffleArray(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }
}

// Initialize the game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new FuturSimpleQuiz();
});