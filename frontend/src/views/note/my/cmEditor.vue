<template>
  <div id="e-cm-editor"></div>
</template>

<script setup>
import {onMounted, ref} from "vue"
import {EditorView, basicSetup} from "codemirror"
import {html} from "@codemirror/lang-html"

let props = defineProps({
  doc: String
})


let cmEditor = ref(null)

onMounted(() => {
  cmEditor = new EditorView({
    doc: props.doc || "",
    extensions: [basicSetup, html()],
    parent: document.getElementById('e-cm-editor')
  })
})

function getDoc() {
  return cmEditor.state.doc.toString()
}

defineExpose({
  getDoc
})

</script>

<style lang="scss">
.cm-editor {
  @apply border-[1px] border-slate-300 rounded
}

.cm-editor.cm-focused {
  @apply border-[1px] border-blue-400 outline-none
}

.cm-editor {
  .cm-gutters {
    @apply rounded-l
  }

  .cm-panels {
    @apply rounded-b
  }

  .cm-search {
    input {
      @apply rounded border-slate-300 outline-0
      focus-visible:border-blue-400
    }

    .cm-button {
      @apply rounded border-slate-300 bg-none
      active:bg-slate-300
    }
  }
}
</style>