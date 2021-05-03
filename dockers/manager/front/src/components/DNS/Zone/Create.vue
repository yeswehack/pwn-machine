<template>
  <q-form @submit="submit">
    <q-card-section>
      <q-input required v-model="form.name" label="Name" class="q-pb-md" />
      <component :is="formChildren.soa" v-model="form.soa" />
    </q-card-section>
    <q-card-section>
      <reset-and-save :modified="modified" @reset="reset" @save="submit" />
    </q-card-section>
  </q-form>
</template>

<script>
import ResetAndSave from "src/components/ResetAndSave.vue";
import SoaForm from "src/components/DNS/Zone/SoaForm.vue";
import DeepForm from "src/mixins/DeepForm.js";
import db from "src/gql";
export default {
  mixins: [DeepForm],
  components: { ResetAndSave },
  formDefinition: {
    name: null,
    soa: SoaForm
  },
  methods: {
    submit() {
      this.$apollo
        .mutate({
          mutation: db.dns.CREATE_ZONE,
          variables: { input: this.form },
          refetchQueries: [{ query: db.dns.GET_ZONES }]
        })
        .then(() => {
          this.$emit("ok");
        });
    }
  }
};
</script>
