import {defineStore} from "pinia"
//
import {deleteNote} from "~/api/note.js"


//
export const useNoteStore = defineStore('note', {
    state: () => ({}),
    actions: {
        toDeleteNote(router, noteId) {
            deleteNote(noteId)
                .then((res) => {
                    router.push({name: 'MyNoteList'})
                })
        },
    },
})