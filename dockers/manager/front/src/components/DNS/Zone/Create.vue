<template>
  <q-form @submit="submit">
    <q-card-section>
      <q-input
        ref="name"
        v-model="form.name"
        label="Name"
        class="q-pb-md"
        :rules="[endsWithDot]"
      />
      <component :is="formChildren.soa" ref="soa" v-model="form.soa" />
    </q-card-section>
    <q-card-section>
      <reset-and-save
        :modified="modified"
        :validate="validate"
        @reset="reset"
        @save="submit"
      />
    </q-card-section>
  </q-form>
</template>

<script>
import ResetAndSave from "src/components/ResetAndSave.vue";
import SoaForm from "src/components/DNS/Zone/SoaForm.vue";
import DeepForm from "src/mixins/DeepForm.js";
import api from "src/api";

export default {
  components: { ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    name: null,
    soa: SoaForm
  },
  methods: {
    endsWithDot: v => v?.endsWith(".") || "Must end with a dot.",
    validate() {
      const validators = [
        this.$refs.name.validate(),
        this.$refs.soa.validate()
      ];
      return validators.every(x => x);
    },
    submit(done) {
      this.mutate({
        mutation: api.dns.zones.CREATE_ZONE,
        variables: { input: this.form },
        refetchQueries: [{ query: api.dns.zones.LIST_ZONES }],
        message: `${this.form.name} created`
      })
        .then(r => this.$emit("ok"))
        .finally(done);
    }
  }
};
</script>
