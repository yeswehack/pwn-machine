<template>
  <q-dialog ref="dialog" class="base-dialog" @hide="onCancel">
    <q-card bordered :style="style">
      <q-card-section>
        <div class="row q-gutter-sm items-center">
          <div class="col col-auto title text-h6  ">
            {{ title }} {{ subtitle ? ":" : "" }}
          </div>
          <div class="col col-auto text-h6 subtitle">
            {{ subtitle }}
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
    width: { type: Number, default: 700 },
    help: { type: String, default: null }
  },
  data() {
    // get the count of base-dialog on screen and use it as dialog depth
    const depth = document.querySelectorAll(".base-dialog:not(:empty)").length;
    const size = this.width - depth * 50;
    const style = { "min-width": `${size}px`, "max-width": "100vw" };
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
    onOk(data) {
      this.$emit("ok", data);
      this.$parent.$emit("ok", data);
      this.hide();
    }
  }
};
</script>

<style lang="scss" scoped>
.title {
  align-self: baseline;
}
.subtitle {
  align-self: baseline;
  font-size: 1em;
  margin-left: 20px;
  opacity: 0.8;
}
</style>
