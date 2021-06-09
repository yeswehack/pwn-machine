<template>
  <div class="column q-col-gutter-md">
    <q-input
      v-model="form.nameserver"
      label="Nameserver"
      :rules="[endsWithDot]"
    />
    <q-input
      v-model="form.postmaster"
      label="Postmaster"
      :rules="[endsWithDot]"
    />
    <div class="row q-gutter-sm">
      <q-input
        v-model.number="form.refresh"
        class="col"
        type="number"
        label="Refresh"
      />
      <q-input
        v-model.number="form.retry"
        class="col"
        type="number"
        label="Retry"
      />
      <q-input
        v-model.number="form.expire"
        class="col"
        type="number"
        label="Expire"
      />
      <q-input
        v-model.number="form.ttl"
        class="col"
        type="number"
        label="TTL"
      />
    </div>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";

export default {
  mixins: [DeepForm],
  formDefinition: {
    nameserver: null,
    postmaster: null,
    refresh: 86400,
    retry: 7200,
    expire: 3600000,
    ttl: 172800
  },
  props: {
    zone: { type: String, default: null }
  },
  methods: {
    endsWithDot: v => v?.endsWith(".") || "Must end with a dot."
  }
};
</script>
