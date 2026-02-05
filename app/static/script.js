class EmpathyEngineUI {
    constructor() {
        this.initElements();
        this.bindEvents();
    }

    initElements() {
        this.textInput = document.getElementById('textInput');
        this.generateBtn = document.getElementById('generateBtn');
        this.clearBtn = document.getElementById('clearBtn');
        this.emotionDisplay = document.getElementById('emotionDisplay');
        this.emotionLabel = document.getElementById('emotionLabel');
        this.emotionDetails = document.getElementById('emotionDetails');
        this.status = document.getElementById('status');
        this.audioPlayer = document.getElementById('audioPlayer');
        this.audioSection = document.getElementById('audioSection');
        this.audioSettings = document.getElementById('audioSettings');
        this.downloadLink = document.getElementById('downloadLink');
    }

    bindEvents() {
        this.generateBtn.addEventListener('click', () => this.generateSpeech());
        this.clearBtn.addEventListener('click', () => this.clearAll());
        this.textInput.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.generateSpeech();
            }
        });
    }

    async generateSpeech() {
        const text = this.textInput.value.trim();
        if (!text) {
            this.showStatus('Enter text first', 'error');
            return;
        }

        this.showStatus('Processing...', 'loading');
        this.hideAudio();
        this.hideEmotion();

        try {
            const response = await fetch('/api/speak', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });

            const result = await response.json();

            if (result.success) {
                this.showEmotion(result.emotion, result.confidence);
                this.showAudio(result.filename, result.settings);
                this.showStatus(
                    `${result.emotion.toUpperCase()} | ${result.settings.rate}wpm | ${(result.settings.volume*100).toFixed(0)}%`,
                    'success'
                );
            } else {
                this.showStatus('Error: ' + result.error, 'error');
            }
        } catch (error) {
            this.showStatus('Connection failed', 'error');
        }
    }

    clearAll() {
        this.textInput.value = '';
        this.hideEmotion();
        this.hideAudio();
        this.hideStatus();
        this.audioPlayer.pause();
    }

    showEmotion(emotion, confidence) {
        this.emotionLabel.textContent = emotion.toUpperCase();
        this.emotionDetails.textContent = `${(confidence * 100).toFixed(1)}% confidence`;
        this.emotionDisplay.classList.remove('hidden');
    }

    showAudio(filename, settings) {
        this.audioPlayer.src = `/audio/${filename}`;
        this.audioPlayer.load();
        this.audioSettings.textContent = `${settings.rate}wpm | ${(settings.volume*100).toFixed(0)}% vol`;
        this.downloadLink.href = `/audio/${filename}`;
        this.downloadLink.download = filename;
        this.audioSection.classList.remove('hidden');
        this.audioPlayer.play().catch(() => {});
    }

    hideAudio() {
        this.audioSection.classList.add('hidden');
        this.audioPlayer.pause();
    }

    showStatus(message, type) {
        this.status.textContent = message;
        this.status.className = `status ${type}`;
        this.status.classList.remove('hidden');
    }

    hideStatus() {
        this.status.classList.add('hidden');
    }

    hideEmotion() {
        this.emotionDisplay.classList.add('hidden');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new EmpathyEngineUI();
});
