<template>
  <base-dialog ref="dialog" title="Create a new service" :subtitle="subtitle">
    <template #default="{ok, cancel}">
      <create-service
        :value="serviceForm"
        @ok="ok"
        @cancel="cancel"
        @updateSubtitle="updateSubtitle"
      />
    </template>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import CreateService from "./Create.vue";

export default {
  components: { CreateService, BaseDialog },
  props: {
    service: { type: Object, default: null }
  },
  data: () => ({ subtitle: null }),
  computed: {
    serviceForm() {
      if (!this.service) {
        return null;
      }
      return { ...this.service, extra: this.service[this.service.type] };
    }
  },
  methods: {
    updateSubtitle(t) {
      this.subtitle = t;
    },
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    }
  }
};
</script>
