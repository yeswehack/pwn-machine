<template>
  <q-select
    ref="select"
    v-model="form"
    label="Service"
    :options="serviceNames"
    clearable
    :rules="[required('You must select a service.')]"
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
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    services: {
      query: api.traefik.services.LIST_SERVICES,
      variables() {
        return { protocols: [this.protocol] };
      },
      update: data => data.traefikServices
    }
  },
  props: { protocol: { type: String, default: null } },
  computed: {
    serviceNames() {
      return (this.services ?? []).map(s => s.name);
    }
  },
  methods: {
    createService() {
      this.$q
        .dialog({
          component: ServiceDialog,
          parent: this
        })
        .onOk(() => {
          this.form = "";
        });
    },
    validate() {
      return this.$refs.select.validate();
    }
  }
};
</script>
