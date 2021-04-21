<template>
  <q-dialog  ref="dialog" @hide="onDialogHide">
    <q-card bordered style="min-width: 600px">
      <q-card-section>
        <div class="row items-center">
          <div class="text-h6">Create a new service</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <q-card-section class="q-gutter-sm">
        <q-input v-model="form.name" required label="Name" />
        <q-select v-model="form.protocol" :options="protocols" label="Protocol" />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn color="warning" label="Cancel" @click="onCancelClick" />
        <q-btn color="positive" label="Create" @click="onOKClick" />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script>
export default {
  data() {
    const form = {};
    const protocols = ["http", "tcp", "udp"];
    return { form, protocols };
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

    onOKClick() {
      this.$emit("ok");
      this.hide();
    },

    onCancelClick() {
      this.hide();
    }
  }
};
</script>
