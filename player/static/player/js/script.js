import {HttpTool} from "./requests.js";

// inspired by https://github.com/goldfire/howler.js/tree/master/examples/player

// Cache references to DOM elements.
const howler = document.getElementById('howler');
const track = document.getElementById('track');
const timer = document.getElementById('timer');
const duration = document.getElementById('duration');
const playButton = document.getElementById('play-button');
const pauseButton = document.getElementById('pause-button');
const backButton = document.getElementById('skip-back-button');
const forwardButton = document.getElementById('skip-forward-button');



const playlist = getObjectByElementId("playlist");
console.dir(playlist)

const cookies = HttpTool.parseCookies();



const eventConfig = {"bubbles":true, "cancelable":true};


const pauseEvent =      new CustomEvent('pause', eventConfig)
const skipPrevEvent =   new CustomEvent('skipPrev', eventConfig)
const skipNextEvent =   new CustomEvent('skipNext', eventConfig)
const loadEvent =       new CustomEvent('load', eventConfig)

class Player {
    /**
     * Player class containing the state of our playlist and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} playlist Array of objects with playlist track details ({title, file, howl}).
     */
    constructor(playlist) {

        this.playlist = playlist;
        this.index = 0;

        this.currentTrackId = playlist.tracks[0].id
        // Display the title of the first track.
        // track.innerHTML = '1. ' + playlist[0].title;
    }

    /**
     * Play a track in the playlist.
     * @param trackId
     */
    play(trackId) {
        const _this = this;

        trackId = trackId || _this.currentTrackId

        const detail = {
            trackId: trackId,
            playlistId: this.playlist.id
        }
        dispatchEvent(new CustomEvent('play', {bubbles: true, detail: detail}))

        const track = _this.playlist.tracks.filter(track => track.id === trackId)[0];


        let sound;
        // If we already loaded this track, use the current one.
        // Otherwise, setup and load a new Howl.
        if (track.howl) {
            sound = track.howl;
        } else {
            sound = track.howl = new Howl({
                src: [`${window.location.origin}/media/${track.audio_file}`],
                html5: true,
                onload:     function () { dispatchEvent(loadEvent) },
                onend:      function () {_this.skip('next');},
            });
        }

        // Begin playing the sound.
        sound.play();
        _this.currentTrackId = trackId;
    }

    /**
     * Pause the currently playing track.
     */
    pause() {
        const _this = this;

        // Get the Howl we want to manipulate.
        const track = _this.playlist.tracks.filter(track => track.id === _this.currentTrackId)[0];

        // Pause the sound.
        track.howl.pause();
        dispatchEvent(pauseEvent)
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
            dispatchEvent(skipPrevEvent)
        } else {
            index = self.index + 1;
            if (index >= self.playlist.length) {
                index = 0;
            }
            dispatchEvent(skipNextEvent)
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
    const element = document.getElementById(elementId).textContent;
    return JSON.parse(element);
}

const player = new Player(playlist)

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

addEventListener('play', (e) => {
    console.log('play event fired.')
    console.dir(e.detail)
    playButton.style.display = 'none';
    pauseButton.style.display = 'block';

    HttpTool.updateLastSongPlayed(e.detail.playlistId, e.detail.trackId, cookies)
        .then(r => console.log(r))
        .catch(e => console.error(e))
})

addEventListener('pause', (e) => {
    console.log('pause event fired.')
    playButton.style.display = 'block';
    pauseButton.style.display = 'none';
})
