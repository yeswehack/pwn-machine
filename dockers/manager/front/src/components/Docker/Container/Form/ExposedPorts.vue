<template>
  <q-expansion-item
    icon="cable"
    label="Exposed ports"
    :caption="`${form.length} port(s)`"
  >
    <q-separator />
    <q-card>
      <q-card-section>
        <component
          :is="formChildren"
          v-model="form"
          :default="{ protocol: 'tcp', targets: [] }"
          :titles="['Container port', 'Protocol', 'Targets']"
          grid-format="150px 100px auto"
          :readonly="readonly"
        >
          <template #containerPort="props">
            <q-input
              v-model.number="props.model.containerPort"
              mask="#####"
              :rules="[validatePort]"
              label="Container port"
              v-bind="props"
              @input="addPort(props.model)"
            />
          </template>
          <template #protocol="props">
            <q-select
              v-model="props.model.protocol"
              :options="['tcp', 'udp']"
              :rules="[required()]"
              label="Protocol"
              v-bind="props"
            />
          </template>

          <template #targets="props">
            <q-select
              v-model="props.model.targets"
              label="Targets"
              use-chips
              new-value-mode="add"
              use-input
              hide-dropdown-icon
              multiple
              outlined
              v-bind="props"
            />
          </template>
          <template #display-targets="{targets}">
            {{ targets && targets.join(", ") || "Not forwarded" }}
          </template>
        </component>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";

export default {
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false },
    container: { type: Object, default: null }
  },
  formDefinition: ListInput,
  methods: {
    validatePort(p) {
      const max = 2 ** 16 - 1;
      return (
        (Number.isInteger(p) && p >= 0 && p <= max) ||
        `Must be in range 0 - ${max}`
      );
    },
    addPort(model) {
      model.targets =
        this.validatePort(model.containerPort) === true
          ? [`0.0.0.0:${model.containerPort}`]
          : [];
    }
  }
};
</script>
