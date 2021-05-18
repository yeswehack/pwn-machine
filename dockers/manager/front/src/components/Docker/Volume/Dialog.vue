<template>
  <base-dialog
    ref="dialog"
    title="Create a new docker volume"
    help="https://docs.docker.com/engine/reference/commandline/volume_create/"
  >
    <template #default="{ok, cancel}">
      <create-volume :value="volume" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateVolume from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";

export default {
  components: { CreateVolume, BaseDialog },
  props: {
    volume: { type: Object, default: null }
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
