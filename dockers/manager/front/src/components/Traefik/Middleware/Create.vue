<template>
  <q-form @submit="submit">
    <q-card-section class="q-col-gutter-md" 
        v-if="!edit">
      <q-input
        v-model="form.name"
        required
        label="Name"
        :rule="[nonEmpty]"
      />
      <q-select
        v-model="form.type"
        use-input
        input-debounce="0"
        :options="middlewaresTypes"
        :rules="[nonEmptyArray]"
        label="Type"
      />
    </q-card-section>

    <q-card-section v-if="form.type">
      <Middleware ref="middlewareForm" v-model="form.extra" :type="form.type" />
    </q-card-section>
    <q-card-actions align="right">
      <q-btn
        color="warning"
        label="Cancel"
        @click="$emit('cancel')"
        v-if="!edit"
      />
      <q-btn
        color="positive"
        type="submit"
        :loading="loading"
        :label="okBtnLabel"
      />
    </q-card-actions>
  </q-form>
</template>

<script>
import db from "src/gql";
import { extend } from "quasar";
import Middleware from "src/components/Traefik/Middleware/Middleware.vue";
import mdinfo from "src/components/Traefik/Middleware/definitions.json";

export default {
  components: { Middleware },
  props: {
    edit: { type: Boolean, default: false },
    middleware: { type: Object, default: null }
  },
  data() {
    const loading = false;
    const originalForm = {
      name: this.middleware?.name.split("@")[0],
      type: this.middleware?.type,
      extra: this.middleware ? this.middleware[this.middleware.type] : {}
    };
    const form = extend(true, {}, originalForm);

    const cache = {};
    const middlewaresTypes = Object.keys(mdinfo).sort();
    return { form, middlewaresTypes, cache, originalForm, loading };
  },
  computed: {
    okBtnLabel() {
      return this.edit ? "Update" : "Create";
    },
    currentType() {
      return this.form.type;
    }
  },
  watch: {
    currentType(newType, oldType) {
      // keep settings in cache for the components life time
      if (oldType) {
        this.cache[oldType] = this.form.extra;
      }
      if (this.cache.hasOwnProperty(newType)) {
        this.form.extra = this.cache[newType];
      } else {
        this.form.extra = {};
      }
    }
  },
  methods: {
    nonEmpty(val) {
      if (val === null || val === undefined) {
        return "You must make a selection.";
      }
    },
    nonEmptyArray(val) {
      if (val === null || val === undefined || val.length == 0) {
        return "You must make a selection.";
      }
    },
    async createMiddleware() {
      this.loading = true;
      const type = this.form.type;
      const mutation = db.traefik.CREATE_MIDDLEWARE[type];
      const input = {
        name: this.form.name,
        [type]: { ...this.form.extra, __typename: undefined }
      };
      await this.$apollo
        .mutate({
          mutation,
          variables: { input },
          refetchQueries: [{ query: db.traefik.GET_MIDDLEWARES }]
        })
        .then(r => {
          this.$emit("ok");
        });
    },
    async updateMiddleware() {
      const type = this.form.type;
      const mutation = db.traefik.UPDATE_MIDDLEWARE[type];
      const variables = {
        nodeId: this.middleware.nodeId,
        patch: { ...this.form.extra, __typename: undefined }
      };
      await this.$apollo
        .mutate({
          mutation,
          variables,
          refetchQueries: [{ query: db.traefik.GET_MIDDLEWARES }]
        })
        .then(r => {
          this.$emit("ok");
        })
        .catch(r => {
          this.$q.notify({
            message: `Unable to update ${this.middleware.name}.`,
            type: "negative"
          });
        });
    },
    async submit() {
      this.loading = true;
      try {
        if (this.edit) {
          await this.updateMiddleware();
        } else {
          await this.createMiddleware();
        }
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
