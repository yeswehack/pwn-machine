<template>
  <q-card :bordered="popup" class="create-router bg-dark" :class="{ popup }">
    <q-form @submit="submit">
      <q-card-section v-if="!edit">
        <div class="row items-center q-gutter-md">
          <div class="text-h6">Create a new middleware</div>
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

        <q-select
          v-model="form.type"
          use-input
          input-debounce="0"
          @filter="filterType"
          :options="types"
          label="Type"
        />
      </q-card-section>

      <q-card-section>
        <Middleware
          ref="middlewareForm"
          :large="large"
          :name="form.type"
          v-if="form.type"
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
import Vue from "vue";
import Middleware from "src/components/Traefik/Middleware/Middleware.vue";
import mdinfo from "src/components/Traefik/Middleware/definitions.json";

export default {
  components: { Middleware },
  props: {
    edit: {
      type: Boolean,
      default: false
    },
    popup: {
      type: Boolean,
      default: false
    },
    large: {
      type: Boolean,
      default: false
    },
    middlewares: {
      type: Array
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
        type: null
      },
      saveText: this.edit ? "Modify" : "Create",
      connect: true,
      types: Object.keys(mdinfo.middlewares)
    };

    if (this.info != null) {
      this.doReset(data.form);
    }
    return data;
  },
  computed: {},

  methods: {
    filterType(val, update) {
      update(() => {
        const names = Object.keys(mdinfo.middlewares);
        val = val.toLowerCase();
        this.types = names.filter(name => name.toLowerCase().indexOf(val) > -1);
      });
    },
    validateName(name) {
      if (!name) {
        return "Middleware name is required";
      }
      if (!this.$api.traefik.isValidMiddlewareName(name)) {
        return "Middleware name can only contains a-z 0-9 - _ .";
      }
      if (!this.edit || this.form.originalName != name) {
        if (
          this.middlewares.map(s => s.name.split("@")[0]).indexOf(name) > -1
        ) {
          return `A Middleware with this name already exists`;
        }
      }
      return true;
    },
    getSettings(settings, name) {
      for (const [sname, setting] of Object.entries(settings)) {
        if (name.toLowerCase() == sname.toLowerCase()) {
          return setting;
        }
      }
    },
    doReset(target) {
      target.originalName = this.info.name.split("@")[0];
      target.name = target.originalName;
      target.type = this.info.type;

      const settings = this.getSettings(this.info, this.info.type);
      Vue.nextTick(() => {
        this.$refs.middlewareForm.setValue(settings);
      });
    },
    reset() {
      this.doReset(this.form);
    },
    async submit() {
      const middleware = {
        name: this.form.name,
        type: this.form.type,
        settings: this.$refs.middlewareForm.getValue()
      };
      const response = this.edit
        ? this.$api.traefik.updateMiddleware(this.form.originalName, middleware)
        : this.$api.traefik.createMiddleware(middleware);

      if ("error" in response) {
        this.$q.notify({
          color: "negative",
          message: response.error
        });
      } else {
        this.$q.notify({
          color: "positive",
          message: this.edit
            ? `Middleware ${this.form.originalName} modified.`
            : `Middleware ${this.form.name} created.`
        });
        this.$emit("created", response.name);
      }
    }
  }
};
</script>

<style lang="scss">
.popup {
  min-width: 700px;
  max-width: 80vw;
}
.servers-select .q-chip {
  padding: 0.5em 0.8em;
  background-color: $primary;
}
</style>
