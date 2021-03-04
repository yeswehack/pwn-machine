<template>
  <div class="row q-col-gutter-md">
    <div class="col-12">
      <div class="row items-center q-col-gutter-md">
        <div class="text-h6">{{ uncamel(name) }}</div>
        <q-space />
        <a
          class="text-white"
          :href="
            `https://doc.traefik.io/traefik/middlewares/${name.toLowerCase()}/`
          "
          target="_blank"
        >
          <q-icon size="sm" name="help" />
        </a>
      </div>
    </div>
    <div class="col-12">
      <q-separator />
    </div>
    <div
      :class="colSize"
      :key="name"
      v-for="[name, type] of Object.entries(middleware)"
    >
      <Type ref="formTypes" :key="name" :name="name" :type="type" />
    </div>
  </div>
</template>

<script>
import mdinfo from "src/components/Traefik/Middleware/definitions.json";
import Type from "./Type.vue";
export default {
  components: { Type },
  name: "Middleware",
  props: {
    name: {
      type: String,
      default: "addPrefix"
    },
    large: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      colSize: this.large ? "col-6" : "col-12"
    };
  },
  created() {
    this.init();
  },
  watch: {
    name() {
      this.init();
    }
  },
  methods: {
    getMiddleware(name) {
      for (const [tname, middleware] of Object.entries(mdinfo.middlewares)) {
        if (tname.toLowerCase() == name.toLowerCase()) {
          return middleware;
        }
      }
    },
    init() {
      const middleware = this.getMiddleware(this.name);
      const form = {};
      for (const name of Object.keys(middleware)) {
        form[name] = null;
      }
      this.middleware = middleware;
      this.form = form;
    },
    uncamel(str) {
      const s = str
        .replace(/([a-z\d])([A-Z])/g, "$1 $2")
        .replace(/([A-Z]+)([A-Z][a-z\d]+)/g, "$1 $2")
        .toLowerCase();

      return s.charAt(0).toUpperCase() + s.slice(1);
    },
    getSetting(settings, name) {
      for (const [sname, setting] of Object.entries(settings)) {
        if (name.toLowerCase() == sname.toLowerCase()) {
          return setting;
        }
      }
    },
    setValue(settings) {
      for (const type of this.$refs.formTypes) {
        const setting = this.getSetting(settings, type.name);
        if (setting) {
          type.setValue(setting);
        }
      }
    },
    getValue() {
      const value = {};
      for (const type of this.$refs.formTypes) {
        const [name, val] = type.getValue();
        value[name] = val;
      }
      return value;
    }
  }
};
</script>

<style lang="scss" scoped></style>>
