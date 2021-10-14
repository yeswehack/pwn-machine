<template>
  <div class="q-mb-md">
    <div class="text-h6">Records</div>
    <component
      :is="formChildren"
      v-model="form"
      :default="{ enabled: true }"
      :titles="['Record', 'Enabled']"
      grid-format="1fr auto"
      :error="error"
    >
      <template #content="props">
        <q-input
          v-model="props.model.content"
          :rules="[required()]"
          label="New record"
          flat
          v-bind="props"
        />
      </template>
      <template #enabled.nopopup="props">
        <q-toggle
          v-model="props.model.enabled"
          :color="props.model.enabled ? 'positive' : 'negative'"
          class="fit"
          v-bind="props"
        />
        <q-tooltip anchor="top middle" self="bottom middle">
          {{ props.model.enabled ? "Enabled" : "Disabled" }}
        </q-tooltip>
      </template>
    </component>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ListInput from "src/components/ListInput.vue";

export default {
  mixins: [DeepForm],
  props: {
    label: { type: String, default: null }
  },
  data: () => ({ error: null }),
  formDefinition: ListInput,
  methods: {
    validate() {
      if (this.form.length < 1) {
        this.error = "You need at least one record.";
        return false;
      }
      return true;
    }
  }
};
</script>
