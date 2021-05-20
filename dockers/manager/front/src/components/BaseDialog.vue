<template>
  <q-dialog ref="dialog" class="base-dialog" @hide="onCancel">
    <q-card bordered :style="style">
      <q-card-section>
        <div class="row items-center q-gutter-sm">
          <div class="text-h6">{{ title }}</div>
          <q-space />
          <help-link :href="help" v-if="help" />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <slot name="default" v-bind="{ cancel: onCancel, ok: onOk }" />
    </q-card>
  </q-dialog>
</template>

<script>
import HelpLink from "./HelpLink.vue";
export default {
  name: "BaseDialog",
  components: { HelpLink },
  props: {
    title: { type: String, required: true },
    help: { type: String, default: null },
  },
  data() {
    // get the count of base-dialog on screen and use it as dialog depth
    const depth = document.querySelectorAll(".base-dialog:not(:empty)").length;
    const size = 700 - depth * 50
    const style = { width: `${size}px`, "max-width": "80vw" };
    return { style };
  },
  methods: {
    shake() {
      this.$refs.dialog.shake();
    },
    show() {
      this.$refs.dialog.show();
    },
    hide() {
      this.$refs.dialog.hide();
    },
    onCancel() {
      this.$emit("hide");
      this.hide();
    },
    onOk() {
      this.$emit("ok");
      this.hide();
    }
  }
};
</script>
