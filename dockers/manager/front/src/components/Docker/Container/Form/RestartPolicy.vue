<template>
  <div class="row">
    <div class="col">
      <q-select
        v-model="form.name"
        :readonly="readonly"
        :options="options"
        map-options
        emit-value
        label="Restart policy"
      >
        <template v-if="form.name !== 'on-failure'" #after>
          <help-link
            href="https://docs.docker.com/engine/reference/run/#restart-policies---restart"
          />
        </template>
      </q-select>
    </div>
    <div v-if="form.name === 'on-failure'" class="col col-3 q-ml-sm">
      <q-input v-model="form.maximumRetryCount" type="number" label="Max-retry">
        <template #after>
          <help-link
            href="https://docs.docker.com/engine/reference/run/#restart-policies---restart"
          />
        </template>
      </q-input>
    </div>
  </div>
</template>

<script>
import HelpLink from "src/components/HelpLink";
import DeepForm from "src/mixins/DeepForm";

export default {
  components: { HelpLink },
  mixins: [DeepForm],
  formDefinition: {
    name: "no",
    maximumRetryCount: 0
  },
  props: {
    readonly: { type: Boolean, default: false }
  },
  data() {
    const options = [
      {
        label: "No",
        value: "no"
      },
      {
        label: "Always",
        value: "always"
      },
      {
        label: "Unless stopped",
        value: "unless-stopped"
      },
      {
        label: "On failure",
        value: "on-failure"
      }
    ];
    return { options, model: this.value };
  }
};
</script>
