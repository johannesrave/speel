export class HttpTool {
    static updateLastSongPlayed(playlistId: string, trackId: string, cookies: { csrftoken?: any; }) {
        const url = `${window.location.origin}/api/playlists/${playlistId}/`

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
        } as RequestInit;

        console.dir(init)
        return fetch(url, init)
    }

    static parseCookies() {
        console.log("Parsing cookies:")

        if (!(document.cookie && document.cookie !== '')) {
            return {};
        }

        const keyValueStrings = document.cookie.split(';')
        const cookies = keyValueStrings.reduce((obj, string) => {
            const match = string.trim().match(/(\w+)=(.*)/);
            if (match) {
                console.log(match)
                const [_, cookieName, value] = match
                return {...obj, [cookieName]: decodeURIComponent(value)}
            }
            return '';
        }, {});
        console.log(cookies)
        return cookies
    }
}