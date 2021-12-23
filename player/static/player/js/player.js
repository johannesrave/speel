import {HttpTool} from "./requests.js";

/*!
* inspired by https://github.com/goldfire/howler.js/tree/master/examples/player
*/

// Cache references to DOM elements.
const track = document.getElementById('track');
const timer = document.getElementById('timer');
const duration = document.getElementById('duration');
const playButton = document.getElementById('play-button');
const pauseButton = document.getElementById('pause-button');
const backButton = document.getElementById('skip-back-button');
const forwardButton = document.getElementById('skip-forward-button');

const cookies = HttpTool.parseCookies();

class Player {
    /**
     * Player class containing the state of our playlist and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} playlist Array of objects with playlist track details ({title, file, howl}).
     * @param {String} playlistId UUID of the playlist on the server, so it can be updated with last_track_played
     */
    constructor(playlist, playlistId) {

        this.playlist = playlist;
        this.playlistId = playlistId;
        this.index = 0;

        // Display the title of the first track.
        track.innerHTML = '1. ' + playlist[0].title;
    }

    /**
     * Play a track in the playlist.
     * @param {Number} index Index of the track in the playlist (leave empty to play the first or current).
     */
    play(index) {
        const self = this;
        let sound;

        index = typeof index === 'number' ? index : self.index;
        const data = self.playlist[index];

        // If we already loaded this track, use the current one.
        // Otherwise, setup and load a new Howl.
        if (data.howl) {
            sound = data.howl;
        } else {
            sound = data.howl = new Howl({
                src: [data.file],
                html5: true, // Force to HTML5 so that the audio can stream in (best for large files).
                onplay: function () {
                    // Display the duration.
                    duration.innerHTML = self.formatTime(Math.round(sound.duration()));

                    pauseButton.style.display = 'block';

                    // Send currently playing track to server
                    HttpTool.updateLastSongPlayed(playlistId, index, cookies)
                        .then(r => console.log(r))
                        .catch(e => console.error(e))
                },
                onload: function () {
                    // Start the wave animation.
                    // wave.container.style.display = 'block';
                    // loading.style.display = 'none';
                },
                onend: function () {
                    self.skip('next');
                },
                onpause: function () {
                },
                onstop: function () {
                },
                onseek: function () {
                }
            });
        }

        // Begin playing the sound.
        sound.play();

        // Update the track display.
        track.innerHTML = (index + 1) + '. ' + data.title;

        // Show the pause button.
        if (sound.state() === 'loaded') {
            playButton.style.display = 'none';
            pauseButton.style.display = 'block';
        } else {
            playButton.style.display = 'none';
            pauseButton.style.display = 'none';
        }

        // Keep track of the index we are currently playing.
        self.index = index;
    }

    /**
     * Pause the currently playing track.
     */
    pause() {
        const self = this;

        // Get the Howl we want to manipulate.
        const sound = self.playlist[self.index].howl;

        // Pause the sound.
        sound.pause();

        // Show the play button.
        playButton.style.display = 'block';
        pauseButton.style.display = 'none';
    }

    /**
     * Skip to the next or previous track.
     * @param  {String} direction 'next' or 'prev'.
     */
    skip(direction) {
        const self = this;

        // Get the next track based on the direction of the track.
        let index = 0;
        if (direction === 'prev') {
            index = self.index - 1;
            if (index < 0) {
                index = self.playlist.length - 1;
            }
        } else {
            index = self.index + 1;
            if (index >= self.playlist.length) {
                index = 0;
            }
        }

        self.skipTo(index);
    }

    /**
     * Skip to a specific track based on its playlist index.
     * @param  {Number} index Index in the playlist.
     */
    skipTo(index) {
        const self = this;

        // Stop the current track.
        if (self.playlist[self.index].howl) {
            self.playlist[self.index].howl.stop();
        }

        // Play the new track.
        self.play(index);
    }

    /**
     * Format the time from seconds to M:SS.
     * @param  {Number} secs Seconds to format.
     * @return {String}      Formatted time.
     */
    formatTime(secs) {
        const minutes = Math.floor(secs / 60) || 0;
        const seconds = (secs - minutes * 60) || 0;

        return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    }
}


function getObjectByElementId(elementId) {
    const tracklistJson = document.getElementById(elementId).textContent;
    return JSON.parse(tracklistJson);
}

const trackList = getObjectByElementId("track_list");
console.log(trackList)

const tracklist = trackList.map(track => {
    return {
        'title': track.title,
        'file': window.location.origin + '/media/' + track.audio_file,
        'howl': null
    }
})

const playlistId = getObjectByElementId("playlist_id");
console.log(playlistId)

const player = new Player(tracklist, playlistId)

// Bind our player controls.
playButton.addEventListener('click', function () {
    player.play();
});
pauseButton.addEventListener('click', function () {
    player.pause();
});
backButton.addEventListener('click', function () {
    player.skip('prev');
});
forwardButton.addEventListener('click', function () {
    player.skip('next');
});