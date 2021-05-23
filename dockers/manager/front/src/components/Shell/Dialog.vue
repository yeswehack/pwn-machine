<template>
  <base-dialog ref="dialog" v-bind="$attrs" title="Start a new process">
    <template #default="{ok, cancel}">
      <create-shell :value="defaultValue" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateShell from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";
export default {
  components: { CreateShell, BaseDialog },
  props: {
    container: { type: Object, default: null }
  },
  computed: {
    defaultValue() {
      return {containerName: this.container.name};
    }
  },
  methods: {
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    }
  }
};
</script>
