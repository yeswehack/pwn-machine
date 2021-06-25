<template>
  <div>
    <base-grid-input
      :titles="['Record', 'Enabled']"
      grid-format="1fr auto"
      :entries="form"
      @addEntry="addEntry"
      @removeEntry="removeEntry"
    >
      <template #inputs> </template>
    </base-grid-input>
    <div v-if="0" class="row q-gutter-md items-end">
      <div class="col">
        <q-input
          v-model="form.subnet"
          v-bind="$attrs"
          :readonly="readonly"
          label="Subnet"
        />
      </div>
      <div class="col">
        <q-input
          v-model="form.gateway"
          v-bind="$attrs"
          :readonly="readonly"
          label="Gateway"
        />
      </div>
      <div class="col">
        <q-input
          v-model="form.ipRange"
          v-bind="$attrs"
          :readonly="readonly"
          label="IP Range"
        />
      </div>
      <div v-if="!readonly" class="col col-auto">
        <q-btn
          flat
          icon="eva-close"
          class="q-pa-none"
          dense
          color="negative"
          @click="$emit('delete')"
        />
      </div>
    </div>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: {
    subnet: null,
    ipRange: null,
    gateway: null
  }
};
</script>
