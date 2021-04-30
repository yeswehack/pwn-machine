<template>
  <div>
    <q-input v-model="form.value" :label="uncamel(name)" v-if="type == 'STR'" />
    <q-input
      v-model.number="form.value"
      :label="uncamel(name)"
      type="number"
      v-if="type == 'NUMBER'"
    />
    <q-toggle
      v-model="form.value"
      :label="uncamel(name)"
      v-if="type == 'BOOL'"
    />
    <q-select
      use-input
      multiple
      use-chips
      hide-dropdown-icon
      hint="multiple"
      v-model="form.value"
      new-value-mode="add"
      :label="uncamel(name)"
      v-if="type == 'ARRAY'"
    />
    <div v-if="type == 'PAIR'" class="row q-col-gutter-md">
      <div class="col-12">{{ name }}</div>

      <div class="col-12" :key="idx" v-for="[idx] in this.form.value.entries()">
        <div class="row q-col-gutter-md items-center">
          <q-input
            class="col-auto col-grow"
            v-model="form.value[idx][0]"
            label="key"
          />
          <q-input
            class="col-auto col-grow"
            v-model="form.value[idx][1]"
            label="value"
          />
          <div class="col-1 self-end">
            <q-btn
              round
              color="negative"
              @click="deletePair(idx)"
              title="Delete pair"
              size="sm"
              icon="delete"
            />
          </div>
        </div>
      </div>
      <div class="col-12">
        <q-btn
          round
          color="positive"
          @click="addPair"
          title="Add pair"
          size="sm"
          icon="add"
        />
      </div>
    </div>
    <div v-if="type == 'REF'">
      <q-card-section>
        <div class="text-h6">{{ uncamel(name) }}</div>
      </q-card-section>
      <q-separator />
      <q-card-section
        :key="name"
        v-for="[name, type] of Object.entries(getRef(name))"
      >
        <Type ref="formTypes" :name="name" :type="type" />
      </q-card-section>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
import mdinfo from "src/components/Traefik/Middleware/definitions.json";
export default {
  components: { Type: () => import("./Type.vue") },
  props: {
    name: {type: String, required: true},
    type: {type: [Object, String], required: true},
  },
  data() {
    const form = {};
    if (this.type == "PAIR") {
      form.value = [[null, null]];
    }
    if (this.type == "ARRAY") {
      form.value = [];
    }
    if (["STR", "BOOL", "NUMBER"].includes(this.type)) {
      form.value = null;
    }

    return { form };
  },
  methods: {
    getRef(name) {
      for (const [tname, type] of Object.entries(mdinfo.type)) {
        if (tname.toLowerCase() == name.toLowerCase()) {
          return type;
        }
      }
    },
    uncamel(str) {
      const s = str
        .replace(/([a-z\d])([A-Z])/g, "$1 $2")
        .replace(/([A-Z]+)([A-Z][a-z\d]+)/g, "$1 $2")
        .toLowerCase();

      return s.charAt(0).toUpperCase() + s.slice(1);
    },
    deletePair(idx) {
      this.form.value.splice(idx, 1);
    },
    addPair() {
      this.form.value.push([null, null]);
    },
    setValue(value) {
      if (this.type == "REF") {
        for (const type of this.$refs.formTypes) {
          if (type in value) {
            type.setValue(value[type]);
          }
        }
        return;
      }
      if (this.type == "PAIR") {
        this.form.value = [];
        for (const [k, v] of Object.entries(value)) {
          this.form.value.push([k, v]);
        }
        return;
      }
      this.form.value = value;
    },
    getValue() {
      if (this.type == "REF") {
        const value = {};
        for (const type of this.$refs.formTypes) {
          const [name, v] = type.getValue();
          value[name] = v;
        }
        return [this.name, value];
      }
      return [this.name, this.form.value];
    }
  }
};
</script>

<style></style>
