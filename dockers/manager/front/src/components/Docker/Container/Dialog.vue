<template>
  <base-dialog
    ref="dialog"
    :width="800"
    title="Create a new docker container"
    help="https://docs.docker.com/engine/reference/commandline/container_create/"
  >
    <template #default="{ok, cancel}">
      <create-container :value="container" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import CreateContainer from "./Create.vue";

export default {
  components: { BaseDialog, CreateContainer },
  props: {
    container: { type: Object, default: null }
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
