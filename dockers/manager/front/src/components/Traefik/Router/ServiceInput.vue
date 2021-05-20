<template>
  <q-select
    v-model="form"
    :rules="[nonEmptyArray]"
    :options="serviceNames"
    label="Service"
  >
    <template #after>
      <q-btn
        title="Create a new service"
        round
        dense
        class="bg-green"
        color="positive"
        icon="add"
        @click="createService"
      />
    </template>
  </q-select>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import ServiceDialog from "../Service/Dialog.vue";
export default {
  props: { protocol: { type: String, default: null } },
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    services: {
      query: api.traefik.GET_SERVICES,
      variables() {
        return { protocols: [this.protocol] };
      },
      update: data => data.traefikServices
    }
  },
  computed: {
    serviceNames() {
      return (this.services ?? []).map(s => s.name);
    }
  },
  methods: {
    nonEmptyArray(val) {
      if (val === null || val === undefined || val.length == 0) {
        return "You must make a selection.";
      }
    },
    createService() {
      this.$q.dialog({
        component: ServiceDialog,
        parent: this
      });
    }
  }
};
</script>

<style></style>
