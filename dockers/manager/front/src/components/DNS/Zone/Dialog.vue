<template>
  <base-dialog
    ref="dialog"
    title="Create a new DNS zone"
    help="https://doc.powerdns.com/authoritative/http-api/zone.html"
  >
    <template #default="{ok, cancel}">
      <create-zone :value="zone" @ok="ok" @cancel="cancel" />
    </template>
  </base-dialog>
</template>

<script>
import CreateZone from "./Create.vue";
import BaseDialog from "src/components/BaseDialog.vue";

export default {
  components: { CreateZone, BaseDialog },
  props: {
    zone: { type: Object, default: null }
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
