<template>
  <editor-content class="e-editor" :editor="editor"/>
</template>

<script setup>
import {EditorContent, useEditor} from "@tiptap/vue-3"
import StarterKit from "@tiptap/starter-kit"
import {Image} from "@tiptap/extension-image"
import {Link} from "@tiptap/extension-link"
import {Placeholder} from "@tiptap/extension-placeholder"
import {Table} from "@tiptap/extension-table"
import {TableCell} from "@tiptap/extension-table-cell"
import {TableHeader} from "@tiptap/extension-table-header"
import {TableRow} from "@tiptap/extension-table-row"
import {TaskItem} from "@tiptap/extension-task-item"
import {TaskList} from "@tiptap/extension-task-list"
import {Typography} from "@tiptap/extension-typography"
import {Underline} from "@tiptap/extension-underline"

let props = defineProps({
  notEditable: {
    type: Boolean
  }
})

const editor = useEditor({
  editorProps: {
    attributes: {
      class: 'prose prose-sm sm:prose',
      spellcheck: false,
    }
  },
  extensions: [
    StarterKit, // https://tiptap.dev/api/extensions/starter-kit
    Typography, // https://tiptap.dev/api/extensions/typography
    Placeholder.configure({
      placeholder: '请输入正文'
    }),// https://tiptap.dev/api/extensions/placeholder
    // Node
    Image.configure({
      // inline: true,
      allowBase64: true,
      HTMLAttributes: {
        class: 'e-image'
      }
    }), // https://tiptap.dev/api/nodes/image
    Table.configure({
      resizable: true,
    }), // https://tiptap.dev/api/nodes/table
    TableCell,
    TableHeader,
    TableRow,
    TaskItem.configure({
      nested: true,
    }),// https://tiptap.dev/api/nodes/task-item
    TaskList,  // https://tiptap.dev/api/nodes/task-list
    // Mark
    Link, // https://tiptap.dev/api/marks/link
    Underline, // https://tiptap.dev/api/marks/underline
  ],
  // enablePasteRules: false,
  // injectCSS: false,
  // Events
  // onUpdate: ({editor}) => {
  //   console.log(editor.getHTML());
  // }
  editable: !props.notEditable,
})

defineExpose({
  editor
})
</script>


<style lang="scss">
.ProseMirror {
  @apply max-w-none
  px-3 py-2
  outline-none
}

.ProseMirror[contenteditable="true"] {
  @apply border-[1px] border-slate-300 rounded
  focus:border-blue-400
}


.ProseMirror {
  p.is-editor-empty:first-child::before {
    content: attr(data-placeholder);
    float: left;
    color: #adb5bd;
    pointer-events: none;
    height: 0;
  }

  pre {
    @apply rounded my-3
    text-gray-500
    bg-yellow-50
    whitespace-pre   #{!important}
  }

  ::-webkit-scrollbar {
    /*滚动条整体样式，定义滚动区域大小*/
    @apply w-0.5 h-0.5
  }
}

.e-editor {
  li, p {
    margin: 0;
  }

  ul[data-type="taskList"] {
    list-style: none;
    padding: 0;

    //p {
    //  margin: 0;
    //}

    li {
      display: flex;
      //margin: 0;

      > label {
        flex: 0 0 auto;
        margin-top: 0; // Fix
        margin-right: 0.5rem;
        user-select: none;
      }

      > div {
        flex: 1 1 auto;
        margin-bottom: 0; // Fix
      }
    }
  }

  .e-image {
    border-radius: 4px;
  }
}

</style>