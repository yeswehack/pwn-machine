<template>
  <q-expansion-item v-bind="$attrs">
    <q-separator />
    <q-card>
      <q-card-section>
        <component
          :is="formChildren"
          v-model="form"
          :titles="['Name', 'Value']"
          :readonly="readonly"
        >
          <template #key="props">
            <q-input
              v-model="props.model.key"
              :rules="[required('Name cannot be empty')]"
              label="Name"
              flat
              v-bind="props"
            />
          </template>
          <template #value="props">
            <q-input
              v-model="props.model.value"
              label="Value"
              flat
              v-bind="props"
            />
          </template>
        </component>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ListInput from "src/components/ListInput.vue";

export default {
  mixins: [DeepForm],
  formDefinition: ListInput,
  props: {
    readonly: { type: Boolean, default: false }
  }
};
</script>
