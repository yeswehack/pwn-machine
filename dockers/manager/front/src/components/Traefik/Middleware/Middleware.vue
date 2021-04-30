<template>
  <div class="row q-col-gutter-md">
    <div class="col-12">
      <div class="row items-center q-col-gutter-md">
        <div class="text-h6">{{ title }}</div>
        <q-space />
        <HelpLink :href="helpUrl" />
      </div>
    </div>
    <div class="col-12" :key="name" v-for="[name, type] of fields">
      <generic-field
        ref="formTypes"
        v-model="model[name]"
        :name="name"
        :type="type"
      />
    </div>
  </div>
</template>

<script>
import mdinfo from "src/components/Traefik/Middleware/definitions.json";
import HelpLink from "src/components/HelpLink.vue";
import GenericField from "./GenericField.vue";
export default {
  components: { GenericField, HelpLink },
  props: {
    value: { type: Object, required: true },
    type: { type: String, required: true }
  },
  data() {
    return { model: {} };
  },
  watch: {
    type: {
      immediate: true,
      handler() {
        this.model = this.value;
      }
    },
    model: {
      deep: true,
      handler(v) {
        this.$emit("input", v);
      }
    }
  },
  computed: {
    title() {
      return this.uncamel(this.type);
    },
    definition() {
      return mdinfo[this.type];
    },
    fields() {
      // definition fields sorted alphabetically
      console.log(this.type, mdinfo)
      const keys = Object.keys(this.definition).sort();
      return keys.map(k => [k, this.definition[k]]);
    },
    helpUrl() {
      let path = this.type.toLowerCase();
      if (path == "errors") {
        path = "errorpages";
      }
      return `https://doc.traefik.io/traefik/middlewares/${path}/`;
    }
  },
  methods: {
    getMiddleware(name) {
      for (const [tname, middleware] of Object.entries(mdinfo)) {
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
    }
  }
};
</script>

<style lang="scss" scoped></style>>
