document.addEventListener('DOMContentLoaded', () => {
    const textDisplay = document.getElementById('text-display');
    const audioPlayer = document.getElementById('audio-player');
    const playButton = document.getElementById('play-button');

    let lines = [];
    let currentHighlightIndex = -1;

    // Function to parse timestamp.txt
    async function loadAndParseTimestamps() {
        try {
            const response = await fetch('timestamp.txt');
            const data = await response.text();
            const rawLines = data.split('\n');

            lines = rawLines.map(line => {
                const match = line.match(/\[(\d+):(\d+)\]\s*(.*)/);
                if (match) {
                    const minutes = parseInt(match[1], 10);
                    const seconds = parseInt(match[2], 10);
                    const text = match[3].trim();
                    return {
                        time: minutes * 60 + seconds,
                        text: text
                    };
                }
                return null;
            }).filter(line => line !== null);

            displayLines();
        } catch (error) {
            console.error('Error loading or parsing timestamp.txt:', error);
            textDisplay.textContent = 'Error loading text.';
        }
    }

    // Function to display lines in the text-display div
    function displayLines() {
        textDisplay.innerHTML = '';
        lines.forEach((line, index) => {
            const p = document.createElement('p');
            p.id = `line-${index}`;
            p.textContent = line.text;
            textDisplay.appendChild(p);
        });
    }

    // Event listener for play button
    playButton.addEventListener('click', () => {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playButton.textContent = 'Pause Audio';
        } else {
            audioPlayer.pause();
            playButton.textContent = 'Play Audio';
        }
    });

    // Event listener for audio time updates
    audioPlayer.addEventListener('timeupdate', () => {
        const currentTime = audioPlayer.currentTime;

        for (let i = 0; i < lines.length; i++) {
            const line = lines[i];
            const nextLine = lines[i + 1];

            // Determine if the current line should be highlighted
            const shouldHighlight = currentTime >= line.time &&
                                    (nextLine ? currentTime < nextLine.time : true);

            const lineElement = document.getElementById(`line-${i}`);
            if (lineElement) {
                if (shouldHighlight && currentHighlightIndex !== i) {
                    // Remove highlight from previous line if any
                    if (currentHighlightIndex !== -1) {
                        const prevLineElement = document.getElementById(`line-${currentHighlightIndex}`);
                        if (prevLineElement) {
                            prevLineElement.classList.remove('highlight');
                        }
                    }
                    // Add highlight to current line
                    lineElement.classList.add('highlight');
                    currentHighlightIndex = i;
                } else if (!shouldHighlight && lineElement.classList.contains('highlight')) {
                    // Remove highlight if audio has moved past this line
                    lineElement.classList.remove('highlight');
                }
            }
        }
    });

    // Initial load of timestamps
    loadAndParseTimestamps();
});