<template>
  <q-expansion-item expand-separator icon="settings" label="Extra settings">
    <q-separator />
    <q-card>
      <q-card-section>
        <div class="q-gutter-sm ">
          <q-input :readonly="readonly" v-model="form.command" label="Command" />
          <q-input :readonly="readonly" v-model="form.user" label="User" />
          <restart-policy :readonly="readonly" v-model="form.restartPolicy"/>
          <component :is="formChildren.capAdd" :readonly="readonly" v-model="form.capAdd" />
          <component :is="formChildren.capDrop" :readonly="readonly" v-model="form.capDrop" />
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
  props: {
    readonly: { type: Boolean, default: false }
  },
  mixins: [DeepForm],
  formDefinition: {
    command: null,
    user: null,
    restartPolicy: null,
    capAdd: CapabilitiesAddInput,
    capDrop: CapabilitiesDropInput
  },
  components: { RestartPolicy }
};
</script>
