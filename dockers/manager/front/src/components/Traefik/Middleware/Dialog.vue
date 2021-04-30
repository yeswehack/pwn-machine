<template>
  <q-dialog ref="dialog" @hide="onDialogHide">
    <q-card bordered style="min-width: 600px">
      <q-card-section>
        <div class="row items-center">
          <div class="text-h6">Create a new middleware</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <create-middleware
        :middleware="middleware"
        @ok="onOK"
        @cancel="hide"
      />
    </q-card>
  </q-dialog>
</template>

<script>
import CreateMiddleware from "./Create.vue";
export default {
  components: { CreateMiddleware },
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
