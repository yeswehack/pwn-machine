<template>
  <q-expansion-item expand-separator icon="settings" label="Extra settings">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="column q-gutter-sm ">
          <q-input dense v-model="form.cmd" label="Command" />
          <q-input dense v-model="form.user" label="User" />
          <restart-policy v-model="form.restartPolicy" />
          <capabilities v-model="form.capabilities" />
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
