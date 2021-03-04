<template>
  <div class="q-gutter-sm column">
    <div class="col">
      <q-input dense filled v-model="formData.cmd" label="Command" />
    </div>
    <div class="col">
      <q-input dense filled v-model="formData.user" label="User" />
    </div>
    <div class="col">
      <RestartPolicy v-model="formData.restartPolicy" />
    </div>
    <div class="col">
      <Capabilities v-model="formData.capabilities" />
    </div>
  </div>
</template>

<script>
import RestartPolicy from "./RestartPolicy.vue";
import Capabilities from "./Capabilities.vue";
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  components: { RestartPolicy, Capabilities }
};
</script>

<style></style>
