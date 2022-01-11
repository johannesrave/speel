export class Ajax {
    static updateLastSongPlayed(playlistId, trackId, cookies) {
        const url = `${window.location.origin}/api/playlists/${playlistId}/`;
        const init = {
            method: 'PATCH',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            redirect: 'follow',
            referrer: 'no-referrer',
            headers: {
                'X-CSRFToken': cookies.csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'last_track_played': trackId
            })
        };
        // console.dir(init)
        return fetch(url, init);
    }
    static updateLastTimestampPlayed(playlistId, lastTimestampPlayed, cookies) {
        const url = `${window.location.origin}/api/playlists/${playlistId}/`;
        const init = {
            method: 'PATCH',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            redirect: 'follow',
            referrer: 'no-referrer',
            headers: {
                'X-CSRFToken': cookies.csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'last_timestamp_played': lastTimestampPlayed
            })
        };
        // console.dir(init)
        return fetch(url, init);
    }
    static parseCookies() {
        console.log("Parsing cookies:");
        if (!(document.cookie && document.cookie !== '')) {
            return {};
        }
        const keyValueStrings = document.cookie.split(';');
        const cookies = keyValueStrings.reduce((obj, string) => {
            const match = string.trim().match(/(\w+)=(.*)/);
            if (match) {
                console.log(match);
                const [_, cookieName, value] = match;
                return Object.assign(Object.assign({}, obj), { [cookieName]: decodeURIComponent(value) });
            }
            return '';
        }, {});
        console.log(cookies);
        return cookies;
    }
}
//# sourceMappingURL=ajax.js.map