import {Ajax} from './ajax.js';
import type {Howl, HowlOptions} from './howler'

declare const Howler: { html5PoolSize: number; };
console.dir(Howler);

// Cache references to DOM elements.
const playPauseButton = document.getElementById('player-head');
const playButton = document.getElementById('play-button');
const pauseButton = document.getElementById('pause-button');
const backButton = document.getElementById('player-ear-left');
const forwardButton = document.getElementById('player-ear-right');

const cookies = Ajax.parseCookies();

const audiobook = getObjectByElementId('audiobook');
console.dir(audiobook)

const eventConfig = {"cancelable": true};

const pauseEvent = new CustomEvent('pause', eventConfig)
const skipPrevEvent = new CustomEvent('skipPrev', eventConfig)
const skipNextEvent = new CustomEvent('skipNext', eventConfig)
const loadEvent = new CustomEvent('load', eventConfig)

interface TrackModel {
    howl?: Howl;
    pkid: number,
    id: string,
    title: string,
    duration: number,
    audio_file: string
}

interface AudiobookModel {
    pkid: number,
    id: string,
    name: string,
    image: string,
    last_track_played_id: string,
    last_timestamp_played: number,
    tracks: TrackModel[]
}

class Player {
    private readonly audiobook: AudiobookModel;
    private readonly tracks: TrackModel[];
    private currentIndex: number;
    // private currentTrackId: string;
    private playing: boolean = false;
    private updatingCurrentTime: number | undefined;
    private lastTimestamp: number;

    /**
     * Player class containing the state of our audiobook and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} audiobook Array of objects with audiobook track details ({title, file, howl}).
     */
    constructor(audiobook: AudiobookModel) {

        this.audiobook = audiobook;
        this.tracks = audiobook.tracks;
        if (this.tracks.length < 1) {
            throw 'audiobook is empty.'
        }

        const indexOfLastPlayedTrack = audiobook.tracks
            .findIndex(track => track.id === audiobook.last_track_played_id);
        this.currentIndex = indexOfLastPlayedTrack !== -1 ? indexOfLastPlayedTrack : 0;
        this.lastTimestamp = audiobook.last_timestamp_played
        // this.currentTrackId = audiobook.tracks[this.currentIndex].id;

    }

    currentTimeEvent(detail: any) {
        dispatchEvent(new CustomEvent('updateCurrentTime', {detail: detail}))
    }

    /**
     * Play a track in the audiobook.
     * @param newIndex
     */

    play(newIndex?: number) {
        clearInterval(this.updatingCurrentTime);
        this.playing = true;
        this.currentIndex = newIndex ?? this.currentIndex

        // stop all other tracks playing.
        this.tracks.forEach((track, index) => {
            if (index === this.currentIndex) return;
            track.howl?.stop();
        })

        const track = this.tracks[this.currentIndex]
        // @ts-ignore
        track.howl = track.howl ?? new Howl(this.getOptions(track))


        this.lastTimestamp = this.lastTimestamp ?? 0;
        if (this.lastTimestamp !== 0) {
            track.howl.seek(this.lastTimestamp);
            this.lastTimestamp = 0
        }

        track.howl.play();

        const detail = {
            trackId: track.id,
            audiobookId: this.audiobook.id,
            lastTimestampPlayed: track.howl.seek(),
            track: track,
        }
        dispatchEvent(new CustomEvent('play', {detail: detail}))

        this.updatingCurrentTime = setInterval(this.currentTimeEvent, 3000, detail);
    }

    private getOptions(track: TrackModel): HowlOptions {
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
        this.playing = false;
        const track = this.tracks[this.currentIndex]
        track.howl?.pause();
        dispatchEvent(pauseEvent)
        clearInterval(this.updatingCurrentTime);
    }

    /**
     * Toggle play/pause.
     */
    togglePlayPause() {
        this.playing = !this.playing;

        if (this.playing) {
            this.play()
        } else {
            this.pause()
        }
    }

    /**
     * Skip to the next or previous track.
     * @param  {String} direction 'next' or 'prev'.
     */
    skip(direction: 'prev' | 'next') {

        if (direction === 'prev') {
            this.currentIndex--;
            if (this.currentIndex < 0) {
                this.currentIndex = this.tracks.length - 1;
            }
            dispatchEvent(skipPrevEvent)
        } else if (direction === 'next') {
            this.currentIndex++;
            if (this.currentIndex >= this.tracks.length) {
                this.currentIndex = 0;
            }
            dispatchEvent(skipNextEvent)
        }

        this.skipTo(this.currentIndex);
    }

    /**
     * Skip some seconds head or backwards.
     * @param {number} amount Number of seconds to skip, can be negative.
     */
    seek(amount: number) {
        console.log(`seeking ${amount} seconds`)

        const currentHowl = this.tracks[this.currentIndex]?.howl
        if (!currentHowl) { return; }

        // currentHowl?.pause()

        const currentPosition = currentHowl.seek();
        console.log("currentPosition", currentPosition)
        const newPosition = currentPosition + amount;
        console.log("newPosition", newPosition)

        // if seeking beyond current track, skip to next.
        if (newPosition > currentHowl.duration() - currentHowl.seek()) {
            this.skip('next')
            // this.seek(newPosition - currentHowl.duration() - currentHowl.seek())
        } else if (false) {} else {
            console.log(`seeking to ${newPosition}`)
            currentHowl.pause()
            currentHowl.seek(newPosition)
            currentHowl.play()
        }
    }

    /**
     * Skip to a specific track based on its audiobook index.
     * @param newIndex
     */
    skipTo(newIndex: number) {
        this.tracks[this.currentIndex]?.howl?.stop()
        this.play(newIndex);
    }

    /**
     * Format the time from seconds to M:SS.
     * @param  {Number} secs Seconds to format.
     * @return {String}      Formatted time.
     */
    formatTime(secs: number) {
        const minutes = Math.floor(secs / 60) || 0;
        const seconds = (secs - minutes * 60) || 0;

        return minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
    }
}


function getObjectByElementId(elementId: string) {
    const element = document.getElementById(elementId);
    if (element) {
        return JSON.parse(element.textContent as string);
    }
}

const player = new Player(audiobook)

// Bind our player controls.
playPauseButton!.addEventListener('click', function () {
    console.log('playPause event fired.')
    player.togglePlayPause();
});
backButton!.addEventListener('click', function () {
    // console.log("skipping to last track")
        console.log("rewind event fired")
        player.seek(-15);
    // player.skip('prev');
});
forwardButton!.addEventListener('click', function () {
    // player.skip('next');
    console.log("seek event fired")
    player.seek(15);
});

const perdiodicallyPatchAudiobook = (audiobookId: string, currentTime: number) => {
    return setInterval(() => {
        Ajax.updateLastTimestampPlayed(audiobookId, currentTime, cookies)
            .catch((e: Error) => console.error(e))
    }, 5000, audiobookId, currentTime);
};

addEventListener('play', (e: Event) => {
    const detail = (e as CustomEvent).detail
    console.log('play event fired.')
    playButton!.style.display = 'none';
    pauseButton!.style.display = 'block';

    Ajax.updateLastSongPlayed(detail.audiobookId, detail.trackId, cookies)
        .catch((e: Error) => console.error(e));

    Ajax.updateLastTimestampPlayed(detail.audiobookId, detail.lastTimestampPlayed, cookies)
        .catch((e: Error) => console.error(e))
})

addEventListener('updateCurrentTime', (e: Event) => {
    const detail = (e as CustomEvent).detail
    console.log('updateCurrentTime event fired.')

    const lastTimestampPlayed = detail.track.howl.seek();

    Ajax.updateLastTimestampPlayed(detail.audiobookId, lastTimestampPlayed, cookies)
        .catch((e: Error) => console.error(e))
})

addEventListener('pause', (e) => {
    console.log('pause event fired.')
    playButton!.style.display = 'block';
    pauseButton!.style.display = 'none';
})

