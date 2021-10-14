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
          {{ caption }}
        </q-item-label>
      </q-item-section>
      <q-item-section side>
        <help-link
          href="https://docs.docker.com/engine/reference/commandline/network_create/#bridge-driver-options"
        />
      </q-item-section>
    </template>
    <q-separator />
    <q-card>
      <q-card-section>
        <component
          :is="formChildren"
          v-model="form"
          :titles="['Subnet', 'Gateway', 'IP Range']"
          :readonly="readonly"
        >
          <template #subnet="props">
            <q-input
              v-model="props.model.subnet"
              :rules="[required()]"
              label="Subnet"
              flat
              v-bind="props"
            />
          </template>
          <template #gateway="props">
            <q-input
              v-model="props.model.gateway"
              label="Gateway"
              flat
              v-bind="props"
            />
          </template>
          <template #ipRange="props">
            <q-input
              v-model="props.model.ipRange"
              label="IP Range"
              flat
              v-bind="props"
            />
          </template>
        </component>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import HelpLink from "src/components/HelpLink.vue";
import ListInput from "src/components/ListInput.vue";

export default {
  components: { HelpLink },
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: ListInput,
  computed: {
    caption() {
      if (this.form.length === 0) {
        return "Automatic";
      }
      return `${this.form.length} setting(s)`;
    }
  }
};
</script>
