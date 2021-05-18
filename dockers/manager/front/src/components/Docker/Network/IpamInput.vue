<template>
  <q-expansion-item expand-separator :caption="caption">
    <template #header>
      <q-item-section avatar>
        <q-avatar icon="eva-share-outline" />
      </q-item-section>
      <q-item-section>
        <q-item-label>
          IPAM Settings
        </q-item-label>
        <q-item-label caption>
          {{caption}}
        </q-item-label>
      </q-item-section>
      <q-item-section side>
        <help-link href="https://docs.docker.com/engine/reference/commandline/network_create/#bridge-driver-options" />
      </q-item-section>
    </template>
    <q-separator />
    <q-card>
      <q-card-section>
        <q-input v-bind="$attrs" v-model="form.subnet" label="Subnet" />
        <q-input
          v-bind="$attrs"
          :disable="!form.subnet"
          v-model="form.range"
          label="Range"
        />
        <q-input v-bind="$attrs" v-model="form.gateway" label="Gateway" />
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import HelpLink from "src/components/HelpLink.vue";
export default {
  components: { HelpLink },
  mixins: [DeepForm],
  formDefinition: {
    subnet: null,
    range: null,
    gateway: null
  },
  computed: {
    caption() {
      return this.form.subnet || this.form.gateway ? "custom" : "automatic";
    }
  }
};
</script>

<style></style>
