<template>
  <q-form @submit="submit">
    <q-tab-panels v-model="panel" animated>
      <q-tab-panel name="chooseType">
        <q-input
          v-model="form.name"
          label="Name"
          required
          :rule="[required('You must make a selection.')]"
        />
        <q-select
          v-model="form.type"
          label="Type"
          use-input
          :options="middlewaresTypes"
          :rules="[required('You must make a selection.')]"
          input-debounce="0"
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
import ResetAndSave from "src/components/ResetAndSave.vue";

export function getCreateComponent(value) {
  return forms[value?.type];
}

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    type: "addPrefix",
    extra: getCreateComponent
  },
  props: { middleware: { type: Object, default: null } },
  data() {
    const originalForm = {
      name: this.middleware?.name.split("@")[0],
      type: this.middleware?.type,
      extra: this.middleware ? this.middleware[this.middleware.type] : {}
    };
    const form = extend(true, {}, originalForm);
    const middlewaresTypes = Object.keys(forms);
    return {
      form,
      middlewaresTypes,
      cache: {},
      originalForm,
      panel: "chooseType"
    };
  },
  computed: {
    currentType() {
      return this.form.type;
    },
    createComponent() {
      return getCreateComponent(this.form);
    }
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
    submit(done) {
      const input = { name: this.form.name, [this.form.type]: this.form.extra };
      this.mutate({
        mutation: api.traefik.middlewares.CREATE_MIDDLEWARE[this.form.type],
        variables: { input },
        refetchQueries: [{ query: api.traefik.middlewares.LIST_MIDDLEWARES }],
        message: `${this.form.name} created.`
      })
        .then(() => {
          this.$emit("ok");
        })
        .finally(done);
    }
  }
};
</script>
