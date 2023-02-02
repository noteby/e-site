<template>
  <div class="e-editor">
    <div class="e-toolbar" v-if="!props.notEditable">
      <div class="e-shortcut-table">
        <el-dropdown trigger="click" :hide-on-click="false">
          <button type="button" class="el-dropdown-link"
                  :disabled="displaySourceCode">表格
          </button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="editor.chain().focus().insertTable(
                                        {rows:3,cols:4,withHeaderRow:true}
                                        ).run()">
                插入表格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().deleteTable().run()"
                                :disabled="!editor.can().deleteTable()">
                删除表格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderColumn().run()"
                                :disabled="!editor.can().toggleHeaderColumn()"
                                divided>
                切换为标题列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderRow().run()"
                                :disabled="!editor.can().toggleHeaderRow()">
                切换为标题行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderCell().run()"
                                :disabled="!editor.can().toggleHeaderCell()">
                切换为标题单元格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addColumnBefore().run()"
                                :disabled="!editor.can().addColumnBefore()"
                                divided>
                左边加一列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addColumnAfter().run()"
                                :disabled="!editor.can().addColumnAfter()">
                右边加一列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().deleteColumn().run()"
                                :disabled="!editor.can().deleteColumn()">
                删除该列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addRowBefore().run()"
                                :disabled="!editor.can().addRowBefore()" divided>
                上边加一行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addRowAfter().run()"
                                :disabled="!editor.can().addRowAfter()">
                下边加一行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().deleteRow().run()"
                                :disabled="!editor.can().deleteRow()">
                删除该行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().mergeOrSplit().run()"
                                :disabled="!editor.can().mergeOrSplit()"
                                divided>
                合并或拆分单元格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().fixTables().run()"
                                :disabled="!editor.can().fixTables()" divided>
                修复所有表格
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>

      <div class="e-shortcut-image">
        <button type="button" @click="openChooseImageDialog()"
                :disabled="displaySourceCode">图片
        </button>
      </div>

      <div class="e-shortcut-source-code">
        <button type="button" @click="onSourceCode">源码</button>
      </div>
    </div>

    <cm-editor v-if="displaySourceCode" ref="cmEditorRef" :doc="editor.getHTML()"/>
    <editor-content v-else class="e-content" :editor="editor"/>
  </div>
</template>

<script setup>
import {ref} from "vue"
import {Editor, EditorContent} from "@tiptap/vue-3"
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
//
import CmEditor from "~/views/note/my/cmEditor.vue"

let props = defineProps({
  notEditable: {
    type: Boolean
  }
})

const editor = new Editor({
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
    }), // https://tiptap.dev/api/extensions/placeholder
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
    }), // https://tiptap.dev/api/nodes/task-item
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

function openChooseImageDialog() {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.onchange = (event) => {
    parseImage(event)
  };
  input.click();
}

async function parseImage(event) {
  const file = event.target.files[0]
  setImage(await imageToBase64(file))
}

function imageToBase64(file) {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = () => {
      resolve(fileReader.result);
    };
    fileReader.onerror = (error) => {
      reject(error);
    };
  });
}

function setImage(url) {
  // const url = window.prompt('URL')
  if (url) {
    editor.chain().focus().setImage({
      src: url,
      height: 200
    }).run()
  }
}

const displaySourceCode = ref(false)

const cmEditorRef = ref(null)

const onSourceCode = () => {
  if (displaySourceCode.value) {
    // console.log(cmEditorRef.value.getDoc())
    editor.commands.setContent(cmEditorRef.value.getDoc())
  }
  displaySourceCode.value = !displaySourceCode.value
}

defineExpose({
  editor
})
</script>


<style lang="scss">
.e-editor {
  .e-toolbar {
    @apply flex
    px-1 pb-1
    text-sm text-gray-500
  }

  .e-toolbar button[disabled] {
    @apply text-gray-300
  }

  .e-shortcut-table {
    .el-dropdown-link {
      @apply text-sm text-gray-500
    }
  }

  .e-shortcut-image,
  .e-shortcut-source-code {
    @apply ml-2
  }
}

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

  table {
    border-collapse: collapse;
    table-layout: fixed;
    width: 100%;
    margin: 0;
    overflow: hidden;

    td, th {
      min-width: 1em;
      border: 2px solid #ced4da;
      padding: 3px 5px;
      vertical-align: top;
      box-sizing: border-box;
      position: relative;

      > * {
        margin-bottom: 0;
      }
    }

    th {
      font-weight: bold;
      text-align: left;
      background-color: #f1f3f5;
    }

    .selectedCell:after {
      z-index: 2;
      position: absolute;
      content: "";
      left: 0;
      right: 0;
      top: 0;
      bottom: 0;
      background: rgba(200, 200, 255, 0.4);
      pointer-events: none;
    }

    .column-resize-handle {
      position: absolute;
      right: -2px;
      top: 0;
      bottom: -2px;
      width: 4px;
      background-color: #adf;
      pointer-events: none;
    }

    p {
      margin: 0;
    }
  }

  .tableWrapper {
    padding: 0.5rem 0;
    overflow-x: auto;
  }
}

.e-content {
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

.el-dropdown-menu__item {
  font-size: 12px;
}

.resize-cursor {
  cursor: col-resize;
}

</style>