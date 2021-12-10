/*!
* inspired by https://github.com/goldfire/howler.js/tree/master/examples/player
*/
// Cache references to DOM elements.
const elms = [
    'track', 'timer', 'duration',
    'playBtn', 'pauseBtn',
    'prevBtn', 'nextBtn',
    'volumeBtn', 'progress', 'bar',
    'playlistBtn', 'playlist', 'list',
    'volume', 'barEmpty', 'barFull', 'sliderBtn'];
elms.forEach(function (elm) {
    window[elm] = document.getElementById(elm);
});

class Player {
    /**
     * Player class containing the state of our playlist and where we are in it.
     * Includes all methods for playing, skipping, updating the display, etc.
     * @param {Array} playlist Array of objects with playlist song details ({title, file, howl}).
     */
    constructor(playlist) {
        this.playlist = playlist;
        this.index = 0;

        // Display the title of the first track.
        track.innerHTML = '1. ' + playlist[0].title;

        // Setup the playlist display.
        playlist.forEach(function (song) {
            const div = document.createElement('div');
            div.className = 'list-song';
            div.innerHTML = song.title;
            div.onclick = function () {
                player.skipTo(playlist.indexOf(song));
            };
            list.appendChild(div);
        });
    }

    /**
     * Play a song in the playlist.
     * @param  {Number} index Index of the song in the playlist (leave empty to play the first or current).
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

                        // Start updating the progress of the track.
                        requestAnimationFrame(self.step.bind(self));

                        // Start the wave animation if we have already loaded
                        // wave.container.style.display = 'block';
                        bar.style.display = 'none';
                        pauseBtn.style.display = 'block';
                    },
                    onload: function () {
                        // Start the wave animation.
                        // wave.container.style.display = 'block';
                        bar.style.display = 'none';
                        // loading.style.display = 'none';
                    },
                    onend: function () {
                        // Stop the wave animation.
                        // wave.container.style.display = 'none';
                        bar.style.display = 'block';
                        self.skip('next');
                    },
                    onpause: function () {
                        // Stop the wave animation.
                        // wave.container.style.display = 'none';
                        bar.style.display = 'block';
                    },
                    onstop: function () {
                        // Stop the wave animation.
                        // wave.container.style.display = 'none';
                        bar.style.display = 'block';
                    },
                    onseek: function () {
                        // Start updating the progress of the track.
                        requestAnimationFrame(self.step.bind(self));
                    }
                });
            }

            // Begin playing the sound.
            sound.play();

            // Update the track display.
            track.innerHTML = (index + 1) + '. ' + data.title;

            // Show the pause button.
            if (sound.state() === 'loaded') {
                playBtn.style.display = 'none';
                pauseBtn.style.display = 'block';
            } else {
                // loading.style.display = 'block';
                playBtn.style.display = 'none';
                pauseBtn.style.display = 'none';
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
            playBtn.style.display = 'block';
            pauseBtn.style.display = 'none';
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

            // Reset progress.
            progress.style.width = '0%';

            // Play the new track.
            self.play(index);
        }

    /**
     * Set the volume and update the volume slider display.
     * @param  {Number} val Volume between 0 and 1.
     */
    volume(val) {
            const self = this;

            // Update the global volume (affecting all Howls).
            Howler.volume(val);

            // Update the display on the slider.
            const barWidth = (val * 90) / 100;
            barFull.style.width = (barWidth * 100) + '%';
            sliderBtn.style.left = (window.innerWidth * barWidth + window.innerWidth * 0.05 - 25) + 'px';
        }

    /**
     * Seek to a new position in the currently playing track.
     * @param  {Number} per Percentage through the song to skip.
     */
    seek(per) {
            const self = this;

            // Get the Howl we want to manipulate.
            const sound = self.playlist[self.index].howl;

            // Convert the percent into a seek position.
            if (sound.playing()) {
                sound.seek(sound.duration() * per);
            }
        }

    /**
     * The step called within requestAnimationFrame to update the playback position.
     */
    step() {
            const self = this;

            // Get the Howl we want to manipulate.
            const sound = self.playlist[self.index].howl;

            // Determine our current seek position.
            const seek = sound.seek() || 0;
            timer.innerHTML = self.formatTime(Math.round(seek));
            progress.style.width = (((seek / sound.duration()) * 100) || 0) + '%';

            // If the sound is still playing, continue stepping.
            if (sound.playing()) {
                requestAnimationFrame(self.step.bind(self));
            }
        }

    /**
     * Toggle the playlist display on/off.
     */
    togglePlaylist() {
            const self = this;
            const display = (playlist.style.display === 'block') ? 'none' : 'block';

            setTimeout(function () {
                playlist.style.display = display;
            }, (display === 'block') ? 0 : 500);
            playlist.className = (display === 'block') ? 'fadein' : 'fadeout';
        }

    /**
     * Toggle the volume display on/off.
     */
    toggleVolume() {
            const self = this;
            const display = (volume.style.display === 'block') ? 'none' : 'block';

            setTimeout(function () {
                volume.style.display = display;
            }, (display === 'block') ? 0 : 500);
            volume.className = (display === 'block') ? 'fadein' : 'fadeout';
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


const songlistJson = document.getElementById('song_list').textContent;
const songs = JSON.parse(songlistJson);
console.log(songs)


const songlist = songs.map(song => {
        return {
            'title': song.title,
            'file': window.location.origin + '/media/' + song.audio_file,
            'howl': null
        }
    }
)
const player = new Player(songlist)

/*

// Setup our new audio player class and pass it the playlist.
const player = new Player([
    {
        title: 'Rave Digger',
        file: 'rave_digger',
        howl: null
    },
    {
        title: '80s Vibe',
        file: '80s_vibe',
        howl: null
    },
    {
        title: 'Running Out',
        file: 'running_out',
        howl: null
    }
]);

*/
// Bind our player controls.
playBtn.addEventListener('click', function () {
    player.play();
});
pauseBtn.addEventListener('click', function () {
    player.pause();
});
prevBtn.addEventListener('click', function () {
    player.skip('prev');
});
nextBtn.addEventListener('click', function () {
    player.skip('next');
});
// waveform.addEventListener('click', function (event) {
//     player.seek(event.clientX / window.innerWidth);
// });
playlistBtn.addEventListener('click', function () {
    player.togglePlaylist();
});
playlist.addEventListener('click', function () {
    player.togglePlaylist();
});
volumeBtn.addEventListener('click', function () {
    player.toggleVolume();
});
volume.addEventListener('click', function () {
    player.toggleVolume();
});

// Setup the event listeners to enable dragging of volume slider.
barEmpty.addEventListener('click', function (event) {
    const per = event.layerX / parseFloat(barEmpty.scrollWidth);
    player.volume(per);
});
sliderBtn.addEventListener('mousedown', function () {
    window.sliderDown = true;
});
sliderBtn.addEventListener('touchstart', function () {
    window.sliderDown = true;
});
volume.addEventListener('mouseup', function () {
    window.sliderDown = false;
});
volume.addEventListener('touchend', function () {
    window.sliderDown = false;
});

const move = function (event) {
    if (window.sliderDown) {
        const x = event.clientX || event.touches[0].clientX;
        const startX = window.innerWidth * 0.05;
        const layerX = x - startX;
        const per = Math.min(1, Math.max(0, layerX / parseFloat(barEmpty.scrollWidth)));
        player.volume(per);
    }
};

volume.addEventListener('mousemove', move);
volume.addEventListener('touchmove', move);
