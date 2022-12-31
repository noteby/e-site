import axios from '~/axios'


export function createNote(title, display, content) {
    return axios.post('/v1/own/note/', {
        title, display, content
    })
}

export function updateNote(noteId, title, display, content) {
    return axios.put('/v1/own/note/' + noteId, {title, display, content})
}

export function getNoteForOwn(noteId) {
    return axios.get('/v1/own/note/' + noteId)
}

export function getNoteListForOwn(limit = 100, offset = 0) {
    return axios.get('/v1/own/note/list?limit=' + limit + '&offset=' + offset)
}

export function getNote(noteId) {
    return axios.get('/v1/note/' + noteId)
}

export function getNoteList(limit = 100, offset = 0) {
    return axios.get('/v1/note/list')
}