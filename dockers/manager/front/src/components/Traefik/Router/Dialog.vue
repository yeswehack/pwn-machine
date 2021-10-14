<template>
  <base-dialog ref="dialog" title="Create a new router" v-bind="$attrs">
    <template #default="{ok, cancel}">
      <create-router :value="router" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateRouter from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";

export default {
  components: { CreateRouter, BaseDialog },
  props: {
    router: { type: Object, default: null }
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
