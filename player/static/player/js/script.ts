// @ts-ignore
import {HttpTool} from './requests.js';
import {Howler, Howl} from './index'

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
    private playlist: PlaylistModel;
    private index: number;
    private currentTrackId: string;
    private tracks: TrackModel[];

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
        this.index = 0;
        this.currentTrackId = playlist.tracks[0].id;
    }

    /**
     * Play a track in the playlist.
     * @param trackId
     */
    play(trackId?: string) {
        const _this = this;

        trackId = trackId || _this.currentTrackId

        const track = _this.tracks.find(track => track.id === trackId);
        if (!track) return;

        const sound = this.getHowl(track);

        sound.play();
        _this.currentTrackId = trackId;

        const detail = {
            trackId: trackId,
            playlistId: this.playlist.id
        }
        dispatchEvent(new CustomEvent('play', {detail: detail}))
    }

    /**
     * Pause the currently playing track.
     */
    pause() {
        const _this = this;

        const track = _this.tracks.find(track => track.id === _this.currentTrackId);
        if (!track) return;

        const sound = this.getHowl(track);
        sound.pause();
        dispatchEvent(pauseEvent)
    }

    /**
     * Skip to the next or previous track.
     * @param  {String} direction 'next' or 'prev'.
     */
    skip(direction: 'prev' | 'next') {
        const _this = this;

        const track = _this.tracks.find(track => track.id === _this.currentTrackId);
        if (!track) return;

        const currentIndex = _this.tracks.indexOf(track)

        // Get the next track based on the direction of the track.
        let index = 0;
        if (direction === 'prev') {
            index = currentIndex - 1;
            if (index < 0) {
                index = _this.tracks.length - 1;
            }
            dispatchEvent(skipPrevEvent)
        } else {
            index = currentIndex + 1;
            if (index >= _this.tracks.length) {
                index = 0;
            }
            dispatchEvent(skipNextEvent)
        }

        _this.skipTo(_this.tracks[index].id);
    }

    /**
     * Skip to a specific track based on its playlist index.
     * @param  {Number} index Index in the playlist.
     */
    skipTo(index: string) {
        const _this = this;

        // Stop the current track.
        // if (_this.playlist[_this.index].howl) {
        //     _this.playlist[_this.index].howl.stop();
        // }

        // Play the new track.
        // _this.play(index);
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

    private getHowl(track: TrackModel) {
        const _this = this;
        return track.howl ? track.howl : (
            track.howl = new Howl({
                src: [`${window.location.origin}/media/${track.audio_file}`],
                html5: true,
                onload: function () {
                    dispatchEvent(loadEvent)
                },
                onend: function () {
                    _this.skip('next');
                },
            }));
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
    console.dir(detail)
    playButton!.style.display = 'none';
    pauseButton!.style.display = 'block';

    HttpTool.updateLastSongPlayed(detail.playlistId, detail.trackId, cookies)
        .then((r: any) => console.log(r))
        .catch((e: Error) => console.error(e))
})

addEventListener('pause', (e) => {
    console.log('pause event fired.')
    playButton!.style.display = 'block';
    pauseButton!.style.display = 'none';
})
