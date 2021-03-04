<template>
  <q-card :bordered="popup" class="create-router bg-dark" :class="{ popup }">
    <q-form @submit="submit" @reset="reset">
      <q-card-section>
        <div class="row items-center">
          <div class="text-h6" v-if="!edit">Create a new router</div>
          <div class="text-h6" v-else>Configuration</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup v-if="!edit" />
        </div>
      </q-card-section>
      <q-separator v-if="!edit" />
      <q-card-section class="q-col-gutter-md">
        <q-input
          v-model="form.name"
          :rules="[validateName]"
          required
          label="Name"
        />
        <q-select
          v-model="form.type"
          :options="types"
          label="Type"
          v-on:input="typeChange(form.type)"
        />
        <q-input
          v-if="form.type != 'udp'"
          v-model="form.rule"
          :rules="[validateRule]"
          lazy-rules
          required
          :hint="
            form.type == 'http' ? 'ex: Host(`example.com`)' : 'ex: HostSNI(`*`)'
          "
          label="Rule"
        />
        <q-select
          v-model="form.entrypoints"
          multiple
          :options="getEntrypointsForType(form.type)"
          label="Entrypoints"
        >
        </q-select>
        <q-select
          v-model="form.service"
          :options="servicesNameForType(form.type)"
          label="Service"
        >
          <template #after>
            <q-btn
              title="Create a new service"
              round
              required
              size="sm"
              color="positive"
              icon="add"
              @click="createServiceVisible = true"
            />
          </template>
        </q-select>
      </q-card-section>

      <q-dialog v-model="createServiceVisible">
        <CreateService
          popup
          :services="services_"
          :routers="routers_"
          :entrypoints="entrypoints_"
          v-on:created="serviceCreated"
        />
      </q-dialog>
      <q-card-actions align="right" class="q-pa-md">
        <q-btn
          v-if="edit"
          label="Reset"
          type="reset"
          color="warning"
          flat
          class="q-py-xs q-px-md"
        />
        <q-btn color="positive" type="submit" class="q-py-xs q-px-md">
          {{ this.saveText }}
        </q-btn>
      </q-card-actions>
    </q-form>
  </q-card>
</template>

<script>
import CreateService from "src/components/Traefik/Service/Create.vue";

function filterLowercase(array, val) {
  const needle = val.toLocaleLowerCase();
  return array.filter(v => v.toLocaleLowerCase().indexOf(needle) > -1);
}

export default {
  components: { CreateService },
  props: {
    services: {
      type: Array,
      default: () => []
    },
    routers: {
      type: Array,
      default: () => []
    },
    entrypoints: {
      type: Array,
      default: () => []
    },
    popup: {
      type: Boolean,
      default: false
    },
    edit: {
      type: Boolean,
      default: false
    },
    info: {
      type: Object,
      default: null
    }
  },
  data() {
    const data = {
      form: {
        name: "",
        rule: "",
        entrypoints: [],
        type: "http",
        service: ""
      },
      types: ["http", "tcp", "udp"],
      saveText: this.edit ? "Modify" : "Create",
      originalName: null,
      createServiceVisible: false,
      connect: true,
      services_: this.services,
      routers_: this.routers,
      entrypoints_: this.entrypoints
    };
    if (this.info != null) {
      this.doReset(data.form);
    }
    return data;
  },
  computed: {
    servicesName() {
      return this.services_.map(e => e.name);
    }
  },

  methods: {
    getEntrypointsForType(type) {
      type = type == "http" ? "tcp" : type;
      return this.entrypoints_.filter(e => e.type == type).map(e => e.name);
    },
    serviceCreated(name) {
      this.services_.push({ name });
      this.service = name;
      this.createServiceVisible = false;
    },
    servicesNameForType(type) {
      return this.services_.filter(s => s.type == type).map(s => s.name);
    },
    validateName(name) {
      if (!name) {
        return "Router name is required";
      }
      if (!this.$api.traefik.isValidRouterName(name)) {
        return "Router name can only contains a-z 0-9 - _ .";
      }
      if (!this.edit || this.form.originalName != name) {
        if (this.routers_.map(s => s.name.split("@")[0]).indexOf(name) > -1) {
          return `A Router with this name already exists`;
        }
      }
      return true;
    },
    validateRule(rule) {
      if (!this.$api.traefik.isValidRule(rule)) {
        return `Syntax error`;
      }
    },
    typeChange(type) {
      this.$emit("type-change", type);
      this.form.service = null;
    },
    doReset(target) {
      target.originalName = this.info.name.split("@")[0];
      target.name = target.originalName;
      target.rule = this.info.rule;
      target.type = this.info.type;
      target.entrypoints = this.info.entryPoints;
      target.service = this.info.service;
    },
    reset() {
      this.doReset(this.form);
    },

    submit() {
      const router = {
        name: this.form.name,
        rule: this.form.rule,
        type: this.form.type,
        entrypoints: this.form.entrypoints,
        service: this.form.service
      };
      const response = this.edit
        ? this.$api.traefik.updateRouter(this.form.originalName, router)
        : this.$api.traefik.createRouter(router);

      if ("error" in response) {
        this.$q.notify({
          color: "negative",
          message: response.error
        });
      } else {
        this.$q.notify({
          color: "positive",
          message: this.edit
            ? `Router ${this.form.originalName} modified.`
            : `Router ${this.form.name} created.`
        });
        this.$emit("created", response.name);
      }
    }
  }
};
</script>

<style>
.popup {
  width: 700px;
  max-width: 80vw;
}
</style>
