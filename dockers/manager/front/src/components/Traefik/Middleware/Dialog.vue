<template>
  <base-dialog ref="dialog" title="Create a new middleware" size="600">
    <template #default="{ok, cancel}">
      <create-middleware :value="middleware" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import CreateMiddleware from "./Create.vue";
export default {
  components: { CreateMiddleware, BaseDialog },
  props: {
    middleware: { type: Object, default: null }
  },
  data() {
    return { form: {} };
  },
  methods: {
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    onDialogHide() {
      this.$emit("hide");
    },
    onOK() {
      this.$emit("ok");
      this.hide();
    }
  }
};
</script>
