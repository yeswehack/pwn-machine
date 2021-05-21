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
      <q-card-section v-if="form.length">
        <ipam-input
          @delete="deleteEntry(idx)"
          v-model="form[idx]"
          :key="idx"
          v-bind="$attrs"
          :readonly="readonly"
          v-for="(ipam, idx) of form"
        />
      </q-card-section>
      <q-card-section v-if="!readonly">
        <div class="row q-gutter-md justify-center">
          <div class="col col-auto">
            <q-btn icon="add" color="positive" @click="addEntry" />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import IpamInput from "./IpamInput.vue";
import HelpLink from "src/components/HelpLink.vue";

export default {
  props: { readonly: { type: Boolean, default: false } },
  components: { HelpLink, IpamInput },
  mixins: [DeepForm],
  formDefinition: [],
  computed: {
    caption() {
      return `${this.form.length} setting(s)`;
    }
  },
  methods: {
    addEntry() {
      this.form.push({ subnet: null, gateway: null, ipRange: null });
    },
    deleteEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>

<style></style>
