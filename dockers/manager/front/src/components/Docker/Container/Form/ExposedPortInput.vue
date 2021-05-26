<template>
  <div class="row">
    <div class="col ">
      <q-select
        clearable
        use-input
        ref="portSelect"
        :rules="[required]"
        :options="portOptions"
        new-value-mode="add"
        label="Port to expose"
        v-model.number="form.port"
        emit-value
        @input="input"
      >
        <template v-slot:option="scope">
          <q-item v-bind="scope.itemProps" v-on="scope.itemEvents">
            <q-item-section>
              <q-item-label>{{ scope.opt.port }}</q-item-label>
            </q-item-section>
            <q-item-section avatar>
              {{ scope.opt.protocol }}
            </q-item-section>
          </q-item>
        </template>
      </q-select>
    </div>
    <div class="col" style="max-width: 100px">
      <q-select
        :options="protocolOptions"
        label="Protocol"
        v-model="form.protocol"
      />
    </div>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
export default {
  mixins: [DeepForm],
  formDefinition: {
    port: null,
    protocol: "HTTP"
  },
  props: {
    container: { type: Object, required: false }
  },
  data() {
    return { protocolOptions: ["HTTP", "TCP", "UDP"] };
  },
  methods: {
    input(value) {
      if (value && typeof value == "object") {
        this.form.protocol = value.protocol == "UDP" ? "UDP" : "HTTP";
        this.form.port = value.port;
      }
    },
    required(v) {
      if (!v) {
        return "This field is required";
      }
    },
    validate() {
      return this.$refs.portSelect.validate();
    }
  },
  computed: {
    portOptions() {
      return (this.container?.ports ?? [])
        .filter(p => p.protocol == "TCP")
        .map(p => {
          return {
            label: p.containerPort,
            port: p.containerPort,
            protocol: p.protocol
          };
        });
    }
  }
};
</script>

<style></style>
