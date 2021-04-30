<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card bordered style="min-width: 600px">
      <q-card-section>
        <div class="row items-center">
          <div class="text-h6">Create a new service</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <create-service :service="service" @ok="onOK" @cancel="hide" />
    </q-card>
  </q-dialog>
</template>

<script>
import CreateService from "./Create.vue";
export default {
  components: { CreateService },
  data() {
    const form = {};
    const protocols = ["http", "tcp", "udp"];
    return { form, protocols };
  },
  props: {
    service: { type: Object, default: null }
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
