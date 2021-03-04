<template>
  <q-card :bordered="popup" class="create-router bg-dark" :class="{ popup }">
    <q-form @submit="submit">
      <q-card-section v-if="!edit">
        <div class="row items-center">
          <div class="text-h6">Create a new service</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </div>
      </q-card-section>
      <q-separator v-if="!edit" />
      <q-card-section class="q-col-gutter-md">
        <q-input
          v-model="form.name"
          required
          :rules="[validateName]"
          label="Name"
        />

        <q-select v-model="form.type" :options="types" label="Type" />

        <q-select
          :value="form.servers"
          class="servers-select"
          @new-value="(val, done) => createValue(form.type, val, done)"
          v-model="form.servers"
          placeholder="10.0.0.1:1234"
          label="Servers"
          :hint="
            form.type == 'http'
              ? 'ex: http://10.10.10.10:1234'
              : 'ex: 10.10.10.10:1234'
          "
          use-input
          use-chips
          multiple
          hide-dropdown-icon
          input-debounce="0"
          new-value-mode="add"
          :rules="[validateServers]"
        />
      </q-card-section>
      <q-card-actions align="right" class="q-pa-md">
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md">
          {{ saveText }}
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
function filterLowercase(array, val) {
  const needle = val.toLocaleLowerCase();
  return array.filter(v => v.toLocaleLowerCase().indexOf(needle) > -1);
}

export default {
  props: {
    popup: {
      type: Boolean,
      default: false
    },
    edit: {
      type: Boolean,
      default: false
    },
    services: {
      type: Array,
      default: () => []
    },
    info: {
      type: Object,
      default: null
    }
  },
  data() {
    const data = {
      form: {
        originalName: null,
        name: "",
        servers: [],
        type: "http"
      },
      saveText: this.edit ? "Modify" : "Create",
      connect: true,
      types: ["http", "tcp", "udp"]
    };

    if (this.info != null) {
      this.doReset(data.form);
    }
    return data;
  },
  computed: {},

  methods: {
    createValue(type, val, done) {
      if (type == "http") {
        val = val.match(/^http?:\/\//) ? val : `http://${val}`;
      }
      done(val);
    },
    validateName(name) {
      if (!name) {
        return "Service name is required";
      }
      if (!this.$api.traefik.isValidServiceName(name)) {
        return "Service name can only contains a-z 0-9 - _ .";
      }
      if (!this.edit || this.form.originalName != name) {
        if (this.services.map(s => s.name.split("@")[0]).indexOf(name) > -1) {
          return `A Service with this name already exists`;
        }
      }
      return true;
    },
    validateServers(servers) {
      if (servers.length) {
        return true;
      }
      return "You need at least one server.";
    },
    doReset(target) {
      target.originalName = this.info.name.split("@")[0];
      target.name = target.originalName;
      target.type = this.info.type;
      if (this.info.loadBalancer) {
        target.servers = this.info.loadBalancer.servers.map(s =>
          this.info.type == "http" ? s.url : s.address
        );
      }
    },
    reset() {
      this.doReset(this.form);
    },
    async submit() {
      const service = {
        name: this.form.name,
        type: this.form.type,
        servers: this.form.servers
      };
      const response = this.edit
        ? this.$api.traefik.updateService(this.form.originalName, service)
        : this.$api.traefik.createService(service);

      if ("error" in response) {
        this.$q.notify({
          color: "negative",
          message: response.error
        });
      } else {
        this.$q.notify({
          color: "positive",
          message: this.edit
            ? `Service ${this.form.originalName} modified.`
            : `Service ${this.form.name} created.`
        });
        this.$emit("created", response.name);
      }
    }
  }
};
</script>

<style lang="scss">
.popup {
  width: 500px;
  max-width: 80vw;
}
.servers-select .q-chip {
  padding: 0.5em 0.8em;
  background-color: $primary;
}
</style>
