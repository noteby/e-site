<template>
  <div class="e-editor">
    <div class="e-toolbar" v-if="!props.notEditable">
      <div class="e-shortcut-table">
        <el-dropdown trigger="click" :hide-on-click="false">
          <span class="el-dropdown-link">表格</span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item
                  @click="editor.chain().focus().insertTable(
                            { rows: 3, cols: 4, withHeaderRow: true }
                          ).run()">
                插入表格
              </el-dropdown-item>
              <el-dropdown-item type="button" @click="editor.chain().focus().deleteTable().run()">
                删除表格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderColumn().run()" divided>
                切换为标题列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderRow().run()">
                切换为标题行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().toggleHeaderCell().run()">
                切换为标题单元格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addColumnBefore().run()" divided>
                左边加一列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addColumnAfter().run()">
                右边加一列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().deleteColumn().run()">
                删除该列
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addRowBefore().run()" divided>
                上边加一行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().addRowAfter().run()">
                下边加一行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().deleteRow().run()">
                删除该行
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().mergeOrSplit().run()" divided>
                合并或拆分单元格
              </el-dropdown-item>
              <el-dropdown-item @click="editor.chain().focus().fixTables().run()" divided>
                修复所有表格
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>

    </div>

    <editor-content class="e-content" :editor="editor"/>
  </div>
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