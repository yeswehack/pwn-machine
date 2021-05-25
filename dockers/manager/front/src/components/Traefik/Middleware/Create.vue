<template>
  <q-form @submit="submit">
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="chooseType">
        <q-input v-model="form.name" required label="Name" :rule="[nonEmpty]" />
        <q-select
          v-model="form.type"
          use-input
          input-debounce="0"
          :options="middlewaresTypes"
          :rules="[nonEmptyArray]"
          label="Type"
        />
      </q-tab-panel>
      <q-tab-panel name="enterSettings">
        <component :is="createComponent" v-model="form.extra" />
      </q-tab-panel>
    </q-tab-panels>
    <q-card-section>
      <reset-and-save
        :steps="['chooseType', 'enterSettings']"
        :step.sync="panel"
        :modified="modified"
        @reset="reset"
        @save="submit"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import api from "src/api";
import { extend } from "quasar";
import forms from "./Forms";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from 'src/components/ResetAndSave.vue';

export function getCreateComponent(value) {
  return forms[value?.type] ?? null;
}

export default {
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    type: "addPrefix",
    extra(value) {
      return getCreateComponent(value);
    }
  },
  components: {ResetAndSave},
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
    const middlewaresTypes = Object.keys(forms);
    return {
      form,
      middlewaresTypes,
      cache,
      originalForm,
      loading,
      panel: "chooseType"
    };
  },
  computed: {
    okBtnLabel() {
      return this.edit ? "Update" : "Create";
    },
    currentType() {
      return this.form.type;
    },
    createComponent() {
      return getCreateComponent(this.form);
    },
  },
  watch: {
    currentType(type) {
      const instance = this.instanciateSubForm(
        getCreateComponent(this.form),
        this.form
      );
      this.form.extra = instance.originalForm;
      this.$emit("updateSubtitle", type);
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
      const mutation = api.traefik.middlewares.CREATE_MIDDLEWARE[type];
      const input = {
        name: this.form.name,
        [type]: this.form.extra
      };
      await this.$apollo
        .mutate({
          mutation,
          variables: { input },
          refetchQueries: [{ query: api.traefik.middlewares.LIST_MIDDLEWARES }]
        })
        .then(r => {
          this.$emit("ok");
        });
    },
    async updateMiddleware() {
      const type = this.form.type;
      const mutation = api.traefik.middlewares.UPDATE_MIDDLEWARE[type];
      const variables = {
        nodeId: this.middleware.nodeId,
        patch: this.form.extra
      };
      await this.$apollo
        .mutate({
          mutation,
          variables,
          refetchQueries: [{ query: api.traefik.middlewares.LIST_MIDDLEWARES }]
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
