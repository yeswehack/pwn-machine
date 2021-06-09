<template>
  <base-dialog
    ref="dialog"
    title="Create a new DNS rule"
    help="https://doc.powerdns.com/authoritative/http-api/zone.html#objects"
  >
    <template #default="{ok, cancel}">
      <create-rule :value="rule" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateRule from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";

export default {
  components: { CreateRule, BaseDialog },
  props: {
    rule: { type: Object, default: null }
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
