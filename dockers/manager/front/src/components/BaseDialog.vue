<template>
  <q-dialog ref="dialog" class="base-dialog" @hide="onCancel">
    <q-card bordered :style="style">
      <q-card-section>
        <div class="row items-center q-gutter-sm">
          <div class="col text-h6 title q-pt-none" :data-subtitle="subtitle">
            {{ title }}
          </div>
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
    subtitle: { type: String, default: null },
    help: { type: String, default: null }
  },
  data() {
    // get the count of base-dialog on screen and use it as dialog depth
    const depth = document.querySelectorAll(".base-dialog:not(:empty)").length;
    const size = 700 - depth * 50;
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
<style lang="scss" scoped>
.base-dialog .title {
  position: relative;
  &[data-subtitle] {
    margin-top: -10px;
  }
  &::after {
    content: attr(data-subtitle);
    position: absolute;
    top: 1em;
    margin-top: 8px;
    left: 0px;
    opacity: 0.7;
    font-size: 0.8em;
  }
}
</style>
