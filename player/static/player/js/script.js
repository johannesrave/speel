import { Ajax } from './ajax.js';
// inspired by https://github.com/goldfire/howler.js/tree/master/examples/player
// Cache references to DOM elements.
const playPauseButton = document.getElementById('player-head');
const playButton = document.getElementById('play-button');
const pauseButton = document.getElementById('pause-button');
const backButton = document.getElementById('player-ear-left');
const forwardButton = document.getElementById('player-ear-right');
const cookies = Ajax.parseCookies();
const audiobook = getObjectByElementId('audiobook');
console.dir(audiobook);
const eventConfig = { "cancelable": true };
const pauseEvent = new CustomEvent('pause', eventConfig);
const skipPrevEvent = new CustomEvent('skipPrev', eventConfig);
const skipNextEvent = new CustomEvent('skipNext', eventConfig);
const loadEvent = new CustomEvent('load', eventConfig);
class Player {
    /**
     * Player class containing the state of our audiobook and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} audiobook Array of objects with audiobook track details ({title, file, howl}).
     */
    constructor(audiobook) {
        // private currentTrackId: string;
        this.playing = false;
        this.audiobook = audiobook;
        this.tracks = audiobook.tracks;
        if (this.tracks.length < 1) {
            throw 'audiobook is empty.';
        }
        const indexOfLastPlayedTrack = audiobook.tracks
            .findIndex(track => track.id === audiobook.last_track_played_id);
        this.currentIndex = indexOfLastPlayedTrack !== -1 ? indexOfLastPlayedTrack : 0;
        this.lastTimestamp = audiobook.last_timestamp_played;
        // this.currentTrackId = audiobook.tracks[this.currentIndex].id;
    }
    currentTimeEvent(detail) {
        dispatchEvent(new CustomEvent('updateCurrentTime', { detail: detail }));
    }
    /**
     * Play a track in the audiobook.
     * @param newIndex
     */
    play(newIndex) {
        var _a, _b;
        clearInterval(this.updatingCurrentTime);
        this.playing = true;
        this.currentIndex = newIndex !== null && newIndex !== void 0 ? newIndex : this.currentIndex;
        // stop all other tracks playing.
        this.tracks.forEach((track, index) => {
            var _a;
            if (index === this.currentIndex)
                return;
            (_a = track.howl) === null || _a === void 0 ? void 0 : _a.stop();
        });
        const track = this.tracks[this.currentIndex];
        // @ts-ignore
        track.howl = (_a = track.howl) !== null && _a !== void 0 ? _a : new Howl(this.getOptions(track));
        this.lastTimestamp = (_b = this.lastTimestamp) !== null && _b !== void 0 ? _b : 0;
        if (this.lastTimestamp !== 0) {
            track.howl.seek(this.lastTimestamp);
            this.lastTimestamp = 0;
        }
        track.howl.play();
        const detail = {
            trackId: track.id,
            audiobookId: this.audiobook.id,
            lastTimestampPlayed: track.howl.seek(),
            track: track,
        };
        dispatchEvent(new CustomEvent('play', { detail: detail }));
        this.updatingCurrentTime = setInterval(this.currentTimeEvent, 3000, detail);
    }
    getOptions(track) {
        const _this = this;
        return {
            src: [`${window.location.origin}/media/${track.audio_file}`],
            html5: true,
            onload: () => dispatchEvent(loadEvent),
            onend: () => _this.skip('next'),
        };
    }
    /**
     * Pause the currently playing track.
     */
    pause() {
        var _a;
        this.playing = false;
        const track = this.tracks[this.currentIndex];
        (_a = track.howl) === null || _a === void 0 ? void 0 : _a.pause();
        dispatchEvent(pauseEvent);
        clearInterval(this.updatingCurrentTime);
    }
    /**
     * Toggle play/pause.
     */
    togglePlayPause() {
        this.playing = !this.playing;
        if (this.playing) {
            this.play();
        }
        else {
            this.pause();
        }
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
     * Skip to a specific track based on its audiobook index.
     * @param newIndex
     */
    skipTo(newIndex) {
        var _a, _b;
        (_b = (_a = this.tracks[this.currentIndex]) === null || _a === void 0 ? void 0 : _a.howl) === null || _b === void 0 ? void 0 : _b.stop();
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
const player = new Player(audiobook);
// Bind our player controls.
playPauseButton.addEventListener('click', function () {
    console.log('playPause event fired.');
    player.togglePlayPause();
});
backButton.addEventListener('click', function () {
    player.skip('prev');
});
forwardButton.addEventListener('click', function () {
    player.skip('next');
});
const perdiodicallyPatchAudiobook = (audiobookId, currentTime) => {
    return setInterval(() => {
        Ajax.updateLastTimestampPlayed(audiobookId, currentTime, cookies)
            .catch((e) => console.error(e));
    }, 5000, audiobookId, currentTime);
};
addEventListener('play', (e) => {
    const detail = e.detail;
    console.log('play event fired.');
    playButton.style.display = 'none';
    pauseButton.style.display = 'block';
    Ajax.updateLastSongPlayed(detail.audiobookId, detail.trackId, cookies)
        .catch((e) => console.error(e));
    Ajax.updateLastTimestampPlayed(detail.audiobookId, detail.lastTimestampPlayed, cookies)
        .catch((e) => console.error(e));
});
addEventListener('updateCurrentTime', (e) => {
    const detail = e.detail;
    console.log('updateCurrentTime event fired.');
    const lastTimestampPlayed = detail.track.howl.seek();
    Ajax.updateLastTimestampPlayed(detail.audiobookId, lastTimestampPlayed, cookies)
        .catch((e) => console.error(e));
});
addEventListener('pause', (e) => {
    console.log('pause event fired.');
    playButton.style.display = 'block';
    pauseButton.style.display = 'none';
});
//# sourceMappingURL=script.js.map