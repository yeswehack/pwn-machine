<template>
  <div class="column q-col-gutter-md">
    <q-input v-model="form.nameserver" label="Nameserver" />
    <q-input v-model="form.postmaster" label="Postmaster" />
    <div class="row q-gutter-sm">
      <q-input class="col" v-model.number="form.refresh" type="number" label="Refresh" />
      <q-input class="col" v-model.number="form.retry" type="number" label="Retry" />
      <q-input class="col" v-model.number="form.expire" type="number" label="Expire" />
      <q-input class="col" v-model.number="form.ttl" type="number" label="TTL" />
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
  data() {
    return {};
  }
};
</script>

<style></style>
