<template>
  <div>
    <q-input v-if="isString" :label="label" v-model="model" />
    <q-input
      v-else-if="isNumber"
      type="number"
      :label="label"
      v-model="model"
    />
    <q-toggle v-else-if="isBoolean" v-model="model" :label="label" />
    <q-select
      v-else-if="isStringArray"
      use-input
      multiple
      use-chips
      hide-dropdown-icon
      icon="eva-search"
      v-model="model"
      new-value-mode="add"
      :label="label"
    >
      <template #append>
        <q-icon name="eva-list-outline" />
      </template>
    </q-select>
    <q-expansion-item
      icon="eva-settings-2-outline"
      v-else-if="isObject"
      expand-separator
      :label="label"
    >
      <q-card>
        <q-card-section>
          <generic-field
            ref="formTypes"
            v-model="model[name]"
            :name="name"
            :type="type"
            :key="name"
            v-for="[name, type] of fields"
          />
        </q-card-section>
      </q-card>
    </q-expansion-item>
    <div v-else>{{ name }} {{ type }}</div>
  </div>
</template>

<script>
import { extend } from "quasar";
export default {
  name: "GenericField",
  props: {
    value: { default: null },
    name: { type: String, required: true },
    type: { type: [Object, String], required: true }
  },
  data() {
    return { model: null };
  },
  watch: {
    type: {
      immediate: true,
      handler() {
        this.model = this.deepCopy(this.value) || this.defaultValue;
      }
    },
    model: {
      deep: true,
      handler(v) {
        this.$emit("input", v)
      }
    }
  },
  computed: {
    isString() {
      return this.type == "String";
    },
    isNumber() {
      return this.type == "Int";
    },
    isStringArray() {
      return this.type == "[String]";
    },
    isBoolean() {
      return this.type == "Boolean";
    },
    isObject() {
      return typeof this.type == "object";
    },
    label() {
      return this.uncamel(this.name);
    },
    fields() {
      const keys = Object.keys(this.type).sort();
      return keys.map(k => [k, this.type[k]]);
    },
    defaultValue() {
      if (this.isString) {
        return "";
      }
      if (this.isStringArray) {
        return [];
      }
      if (this.isObject) {
        return {};
      }
      return null;
    }
  },
  methods: {
    deepCopy(v) {
      if (v === null) {
        return null;
      }
      if (Array.isArray(v)) {
        return v.map(e => this.deepCopy(e));
      }
      if (typeof v === "object") {
        return extend(true, {}, v);
      }
      return v;
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

<style lang="scss" scoped>
.subfields {
  position: relative;
}
.subfields::before {
  content: "";
  position: absolute;
  top: 30px;
  bottom: 10px;
  left: 0;
  width: 1px;
  background: #fff;
}
</style>
