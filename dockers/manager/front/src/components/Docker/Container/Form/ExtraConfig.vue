<template>
  <q-expansion-item expand-separator icon="settings" label="Extra settings">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="column q-gutter-sm ">
          <q-input :readonly="readonly" v-model="form.cmd" label="Command" />
          <q-input :readonly="readonly" v-model="form.user" label="User" />
          <restart-policy :readonly="readonly" v-model="form.restartPolicy" />
          <capabilities :readonly="readonly" v-model="form.capabilities" />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import RestartPolicy from "./RestartPolicy.vue";
import Capabilities from "./Capabilities.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  props: {
    readonly: { type: Boolean, default: false }
  },
  mixins: [DeepForm],
  formDefinition: {
    cmd: null,
    user: null,
    restartPolicy: null,
    capabilities: null
  },
  components: { RestartPolicy, Capabilities }
};
</script>

<style></style>
