<template>
  <base-dialog
    ref="dialog"
    title="Create a new docker network"
    help="https://docs.docker.com/engine/api/v1.41/#operation/NetworkCreate"
  >
    <template #default="{ok, cancel}">
      <create-network :value="network" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateNetwork from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";

export default {
  components: { CreateNetwork, BaseDialog },
  props: {
    network: { type: Object, default: null }
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
