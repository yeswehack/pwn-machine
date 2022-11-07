<template>
  <div>
    <div class="text-h6">Weighted services</div>
    <component
      :is="formChildren"
      v-model="form"
      :titles="['Service', 'Weight']"
      :readonly="readonly"
      :error="error"
    >
      <template #name="props">
        <q-select
          v-model="props.model.name"
          :options="serviceOptions"
          :rules="[required()]"
          label="Service"
          flat
          v-bind="props"
        />
      </template>
      <template #weight="props">
        <q-input
          v-model.number="props.model.weight"
          type="number"
          :rules="[required()]"
          label="Weight"
          flat
          v-bind="props"
        />
      </template>
    </component>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ListInput from "src/components/ListInput.vue";
import api from "src/api";

export default {
  mixins: [DeepForm],
  formDefinition: ListInput,
  apollo: {
    services: {
      query: api.traefik.services.LIST_SERVICES,
      variables() {
        return { protocols: [this.protocol] };
      },
      update: data => data.traefikServices
    }
  },
  props: {
    readonly: { type: Boolean, default: false },
    protocol: { type: String, default: null }
  },
  data: () => ({ error: "" }),
  computed: {
    serviceOptions() {
      return (this.services ?? []).map(s => s.name);
    }
  },
  methods: {
    validate() {
      this.error = "";
      if (this.form.length === 0) {
        this.error = "You must choose at least one service";
        return false;
      }
      return true;
    }
  }
};
</script>
