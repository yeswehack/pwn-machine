<template>
  <q-expansion-item expand-separator icon="settings" label="Extra settings">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="q-gutter-sm ">
          <q-input v-model="form.command" :readonly="readonly" label="Command" />
          <q-input v-model="form.user" :readonly="readonly" label="User" />
          <restart-policy v-model="form.restartPolicy" :readonly="readonly"/>
          <component :is="formChildren.capAdd" v-model="form.capAdd" :readonly="readonly" />
          <component :is="formChildren.capDrop" v-model="form.capDrop" :readonly="readonly" />
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import RestartPolicy from "./RestartPolicy.vue";
import CapabilitiesAddInput from "./CapabilitiesAddInput.vue";
import CapabilitiesDropInput from "./CapabilitiesDropInput.vue";
import DeepForm from "src/mixins/DeepForm.js";

export default {
  components: { RestartPolicy },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: {
    command: null,
    user: null,
    restartPolicy: null,
    capAdd: CapabilitiesAddInput,
    capDrop: CapabilitiesDropInput
  }
};
</script>
