import { HttpTool } from './ajax.js';
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
const playlist = getObjectByElementId('playlist');
console.dir(playlist);
const cookies = HttpTool.parseCookies();
const eventConfig = { "cancelable": true };
const pauseEvent = new CustomEvent('pause', eventConfig);
const skipPrevEvent = new CustomEvent('skipPrev', eventConfig);
const skipNextEvent = new CustomEvent('skipNext', eventConfig);
const loadEvent = new CustomEvent('load', eventConfig);
class Player {
    /**
     * Player class containing the state of our playlist and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} playlist Array of objects with playlist track details ({title, file, howl}).
     */
    constructor(playlist) {
        this.playlist = playlist;
        this.tracks = playlist.tracks;
        if (this.tracks.length < 1) {
            throw 'Playlist is empty.';
        }
        this.currentIndex = 0;
        this.currentTrackId = playlist.tracks[this.currentIndex].id;
    }
    /**
     * Play a track in the playlist.
     * @param newIndex
     */
    play(newIndex) {
        var _a;
        this.currentIndex = newIndex !== null && newIndex !== void 0 ? newIndex : this.currentIndex;
        // stop all other tracks playing.
        this.tracks.forEach((track, index) => {
            var _a;
            if (index == this.currentIndex)
                return;
            (_a = track.howl) === null || _a === void 0 ? void 0 : _a.stop();
        });
        const track = this.tracks[this.currentIndex];
        // @ts-ignore
        track.howl = (_a = track.howl) !== null && _a !== void 0 ? _a : new Howl(this.getOptions(track));
        track.howl.play();
        const detail = {
            trackId: track.id,
            playlistId: this.playlist.id
        };
        dispatchEvent(new CustomEvent('play', { detail: detail }));
    }
    getOptions(track) {
        const _this = this;
        return {
            src: [`${window.location.origin}/media/${track.audio_file}`],
            html5: true,
            onload: function () {
                dispatchEvent(loadEvent);
            },
            onend: function () {
                _this.skip('next');
            },
        };
    }
    /**
     * Pause the currently playing track.
     */
    pause() {
        var _a;
        const track = this.tracks[this.currentIndex];
        (_a = track.howl) === null || _a === void 0 ? void 0 : _a.pause();
        dispatchEvent(pauseEvent);
    }
    /**
     * Skip to the next or previous track.
     * @param  {String} direction 'next' or 'prev'.
     */
    skip(direction) {
        if (direction === 'prev') {
            this.currentIndex--;
            if (this.currentIndex < 0) {
                this.currentIndex = this.tracks.length - 1;
            }
            dispatchEvent(skipPrevEvent);
        }
        else if (direction === 'next') {
            this.currentIndex++;
            if (this.currentIndex >= this.tracks.length) {
                this.currentIndex = 0;
            }
            dispatchEvent(skipNextEvent);
        }
        this.skipTo(this.currentIndex);
    }
    /**
     * Skip to a specific track based on its playlist index.
     * @param newIndex
     */
    skipTo(newIndex) {
        this.play(newIndex);
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
    const element = document.getElementById(elementId);
    if (element) {
        return JSON.parse(element.textContent);
    }
}
const player = new Player(playlist);
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
    const detail = e.detail;
    console.log('play event fired.');
    // console.dir(detail)
    playButton.style.display = 'none';
    pauseButton.style.display = 'block';
    HttpTool.updateLastSongPlayed(detail.playlistId, detail.trackId, cookies)
        // .then((r: any) => console.log(r))
        .catch((e) => console.error(e));
});
addEventListener('pause', (e) => {
    console.log('pause event fired.');
    playButton.style.display = 'block';
    pauseButton.style.display = 'none';
});
