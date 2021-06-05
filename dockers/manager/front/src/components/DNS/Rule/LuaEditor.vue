<template>
  <div class="col editor-container">
    <monaco-editor
      v-model="form"
      :options="editorOptions"
      class="editor"
      language="lua"
      theme="vs-dark"
    />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import MonacoEditor from "vue-monaco";

export default {
  components: { MonacoEditor },
  mixins: [DeepForm],
  formDefinition: "",
  data() {
    const editorOptions = {
      minimap: { enabled: false },
      padding: { bottom: 100, top: 100 },
      lineDecorationsWidth: 5,
      lineNumbers: false
    };
    return { editorOptions };
  }
};
</script>

<style lang="scss" scoped>
.editor-container {
  display: grid;
  grid-template-rows: 300px;
  grid-template-columns: 1fr;
}

.editor {
  border: 1px solid rgba(255, 255, 255, 0.28);
  border-radius: 4px;
  overflow: hidden;
  box-sizing: border-box;
}
</style>
