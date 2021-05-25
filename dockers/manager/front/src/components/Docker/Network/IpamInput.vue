<template>
  <div>
    <base-grid-input
      :titles="['Record', 'Enabled']"
      gridFormat="1fr auto"
      :entries="form"
      @addEntry="addEntry"
      @removeEntry="removeEntry"
    >
      <template #inputs> </template>
    </base-grid-input>
    <div class="row q-gutter-md items-end" v-if="0">
      <div class="col">
        <q-input
          v-bind="$attrs"
          :readonly="readonly"
          v-model="form.subnet"
          label="Subnet"
        />
      </div>
      <div class="col">
        <q-input
          v-bind="$attrs"
          :readonly="readonly"
          v-model="form.gateway"
          label="Gateway"
        />
      </div>
      <div class="col">
        <q-input
          v-bind="$attrs"
          :readonly="readonly"
          v-model="form.ipRange"
          label="IP Range"
        />
      </div>
      <div class="col col-auto" v-if="!readonly">
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
  props: { readonly: { type: Boolean, default: false } },
  mixins: [DeepForm],
  formDefinition: {
    subnet: null,
    ipRange: null,
    gateway: null
  }
};
</script>

<style></style>
