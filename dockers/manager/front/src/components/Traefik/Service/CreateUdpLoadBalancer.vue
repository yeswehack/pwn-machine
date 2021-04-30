<template>
  <div class="q-gutter-md">
    <list-input v-model="form.servers" object-key="address" label="Servers" />
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
import ListInput from "src/components/ListInput.vue";
export default {
  components: { ListInput },
  mixins: [DeepForm],
  methods: {
    createDefaultForm(loadbalancer) {
      const form = {
        servers: loadbalancer?.servers ?? [],
      };
      return form;
    }
  }
};
</script>

<style></style>
