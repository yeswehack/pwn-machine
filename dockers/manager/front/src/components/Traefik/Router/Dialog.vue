<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card bordered style="min-width: 600px">
      <q-card-section>
        <div class="row items-center">
          <div class="text-h6">Create a new router</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <create-router :router="router" @ok="onOK" @cancel="hide"/>
    </q-card>
  </q-dialog>
</template>

<script>
import db from "src/gql";
import CreateRouter from "./Create.vue";
export default {
  components: { CreateRouter },
  props: {
    router: { type: Object, default: null }
  },
  apollo: {
    entrypoints: {
      query: db.traefik.GET_ENTRYPOINTS,
      update: data => data.traefikEntrypoints
    },
    services: {
      query: db.traefik.GET_SERVICES,
      update: data => data.traefikServices
    }
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
    },
  }
};
</script>
