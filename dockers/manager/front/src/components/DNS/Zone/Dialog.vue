<template>
  <q-dialog ref="dialog" @hide="onDialogHide" >
    <q-card bordered style="min-width: 600px" >
      <q-card-section>
        <div class="row items-center q-gutter-sm">
          <div class="text-h6">Create a new DNS zone</div>
          <q-space />
          <help-link
            href="https://doc.powerdns.com/authoritative/http-api/zone.html"
          />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator />
      <create-zone :value="zone" @ok="onOK" @cancel="hide" />
    </q-card>
  </q-dialog>
</template>

<script>
import HelpLink from "src/components/HelpLink.vue";
import CreateZone from "./Create.vue";
export default {
  components: { CreateZone, HelpLink },
  props: {
    zone: { type: Object, default: null }
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
