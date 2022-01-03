import {HttpTool} from './ajax.js';
import type {Howl, HowlOptions} from './howler'

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
console.dir(playlist)

const cookies = HttpTool.parseCookies();


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

interface PlaylistModel {
    pkid: number,
    id: string,
    name: string,
    thumbnail_file: string,
    last_track_played_id: string,
    last_timestamp_played: number,
    tracks: TrackModel[]
}

class Player {
    private readonly playlist: PlaylistModel;
    private readonly tracks: TrackModel[];
    private currentIndex: number;
    private currentTrackId: string;

    /**
     * Player class containing the state of our playlist and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} playlist Array of objects with playlist track details ({title, file, howl}).
     */
    constructor(playlist: PlaylistModel) {

        this.playlist = playlist;
        this.tracks = playlist.tracks;
        if (this.tracks.length < 1) {
            throw 'Playlist is empty.'
        }
        this.currentIndex = 0;
        this.currentTrackId = playlist.tracks[this.currentIndex].id;
    }

    /**
     * Play a track in the playlist.
     * @param newIndex
     */

    play(newIndex?: number) {

        this.currentIndex = newIndex ?? this.currentIndex

        // stop all other tracks playing.
        this.tracks.forEach((track, index) => track.howl?.stop())

        const track = this.tracks[this.currentIndex]
        // @ts-ignore
        track.howl = track.howl ?? new Howl(this.getOptions(track))
        track.howl.play();

        const detail = {
            trackId: track.id,
            playlistId: this.playlist.id
        }
        dispatchEvent(new CustomEvent('play', {detail: detail}))
    }

    private getOptions(track: TrackModel): HowlOptions {
        const _this = this;
        return {
            src: [`${window.location.origin}/media/${track.audio_file}`],
            html5: true,
            onload: function () {
                dispatchEvent(loadEvent)
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
        const track = this.tracks[this.currentIndex]
        track.howl?.pause();
        dispatchEvent(pauseEvent)
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
     * Skip to a specific track based on its playlist index.
     * @param newIndex
     */
    skipTo(newIndex: number) {
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

const player = new Player(playlist)

// Bind our player controls.
playButton!.addEventListener('click', function () {
    player.play();
});
pauseButton!.addEventListener('click', function () {
    player.pause();
});
backButton!.addEventListener('click', function () {
    player.skip('prev');
});
forwardButton!.addEventListener('click', function () {
    player.skip('next');
});

addEventListener('play', (e: Event) => {
    const detail = (e as CustomEvent).detail
    console.log('play event fired.')
    // console.dir(detail)
    playButton!.style.display = 'none';
    pauseButton!.style.display = 'block';

    HttpTool.updateLastSongPlayed(detail.playlistId, detail.trackId, cookies)
        // .then((r: any) => console.log(r))
        .catch((e: Error) => console.error(e))
})

addEventListener('pause', (e) => {
    console.log('pause event fired.')
    playButton!.style.display = 'block';
    pauseButton!.style.display = 'none';
})



