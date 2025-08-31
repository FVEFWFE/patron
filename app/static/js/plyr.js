// Minimal Plyr Video Player Implementation
// Self-hosted, no external dependencies

class Plyr {
    constructor(element, options = {}) {
        this.media = element;
        this.options = Object.assign({
            controls: ['play', 'progress', 'volume', 'fullscreen'],
            hideControls: true,
            clickToPlay: true
        }, options);
        
        this.init();
    }
    
    init() {
        // Create wrapper
        this.wrapper = document.createElement('div');
        this.wrapper.className = 'plyr';
        this.media.parentNode.insertBefore(this.wrapper, this.media);
        this.wrapper.appendChild(this.media);
        
        // Create controls
        this.createControls();
        
        // Bind events
        this.bindEvents();
        
        // Set initial state
        this.updatePlayButton();
        this.updateProgress();
    }
    
    createControls() {
        this.controls = document.createElement('div');
        this.controls.className = 'plyr__controls';
        
        // Play button
        if (this.options.controls.includes('play')) {
            this.playButton = document.createElement('button');
            this.playButton.className = 'plyr__control plyr__control--play';
            this.playButton.innerHTML = '▶';
            this.controls.appendChild(this.playButton);
        }
        
        // Progress bar
        if (this.options.controls.includes('progress')) {
            this.progressBar = document.createElement('div');
            this.progressBar.className = 'plyr__progress';
            this.progressFilled = document.createElement('div');
            this.progressFilled.className = 'plyr__progress-filled';
            this.progressBar.appendChild(this.progressFilled);
            this.controls.appendChild(this.progressBar);
        }
        
        // Time display
        this.timeDisplay = document.createElement('div');
        this.timeDisplay.className = 'plyr__time';
        this.timeDisplay.textContent = '0:00 / 0:00';
        this.controls.appendChild(this.timeDisplay);
        
        // Volume
        if (this.options.controls.includes('volume')) {
            this.volumeControl = document.createElement('div');
            this.volumeControl.className = 'plyr__volume';
            this.volumeControl.innerHTML = `
                <button class="plyr__control plyr__control--mute">🔊</button>
                <input type="range" min="0" max="100" value="100" class="plyr__volume-range">
            `;
            this.controls.appendChild(this.volumeControl);
        }
        
        // Fullscreen
        if (this.options.controls.includes('fullscreen')) {
            this.fullscreenButton = document.createElement('button');
            this.fullscreenButton.className = 'plyr__control plyr__control--fullscreen';
            this.fullscreenButton.innerHTML = '⛶';
            this.controls.appendChild(this.fullscreenButton);
        }
        
        this.wrapper.appendChild(this.controls);
    }
    
    bindEvents() {
        // Play/pause
        if (this.playButton) {
            this.playButton.addEventListener('click', () => this.togglePlay());
        }
        
        if (this.options.clickToPlay) {
            this.media.addEventListener('click', () => this.togglePlay());
        }
        
        // Progress
        if (this.progressBar) {
            this.progressBar.addEventListener('click', (e) => this.seek(e));
            this.media.addEventListener('timeupdate', () => this.updateProgress());
        }
        
        // Volume
        if (this.volumeControl) {
            const volumeRange = this.volumeControl.querySelector('.plyr__volume-range');
            const muteButton = this.volumeControl.querySelector('.plyr__control--mute');
            
            volumeRange.addEventListener('input', (e) => {
                this.media.volume = e.target.value / 100;
            });
            
            muteButton.addEventListener('click', () => {
                this.media.muted = !this.media.muted;
                muteButton.innerHTML = this.media.muted ? '🔇' : '🔊';
            });
        }
        
        // Fullscreen
        if (this.fullscreenButton) {
            this.fullscreenButton.addEventListener('click', () => this.toggleFullscreen());
        }
        
        // Media events
        this.media.addEventListener('play', () => this.updatePlayButton());
        this.media.addEventListener('pause', () => this.updatePlayButton());
        this.media.addEventListener('loadedmetadata', () => this.updateTimeDisplay());
        
        // Hide/show controls
        if (this.options.hideControls) {
            let hideTimeout;
            
            this.wrapper.addEventListener('mouseenter', () => {
                clearTimeout(hideTimeout);
                this.controls.style.opacity = '1';
            });
            
            this.wrapper.addEventListener('mouseleave', () => {
                if (!this.media.paused) {
                    hideTimeout = setTimeout(() => {
                        this.controls.style.opacity = '0';
                    }, 2000);
                }
            });
        }
    }
    
    togglePlay() {
        if (this.media.paused) {
            this.media.play();
        } else {
            this.media.pause();
        }
    }
    
    updatePlayButton() {
        if (this.playButton) {
            this.playButton.innerHTML = this.media.paused ? '▶' : '❚❚';
        }
    }
    
    seek(e) {
        const rect = this.progressBar.getBoundingClientRect();
        const percent = (e.clientX - rect.left) / rect.width;
        this.media.currentTime = percent * this.media.duration;
    }
    
    updateProgress() {
        if (this.progressFilled && this.media.duration) {
            const percent = (this.media.currentTime / this.media.duration) * 100;
            this.progressFilled.style.width = percent + '%';
        }
        this.updateTimeDisplay();
    }
    
    updateTimeDisplay() {
        if (this.timeDisplay) {
            const current = this.formatTime(this.media.currentTime);
            const duration = this.formatTime(this.media.duration);
            this.timeDisplay.textContent = `${current} / ${duration}`;
        }
    }
    
    formatTime(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    toggleFullscreen() {
        if (!document.fullscreenElement) {
            this.wrapper.requestFullscreen().then(() => {
                this.wrapper.classList.add('plyr--fullscreen');
            });
        } else {
            document.exitFullscreen().then(() => {
                this.wrapper.classList.remove('plyr--fullscreen');
            });
        }
    }
}

// Export for use
window.Plyr = Plyr;