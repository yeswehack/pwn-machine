<template>
  <q-form @submit="submit">
    <q-card-section>
      <q-input
        required
        v-model="form.name"
        label="Name"
        class="q-pb-md"
        :rules="[endsWithDot]"
      />
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
import api from "src/api";
import { notify } from "src/utils";
export default {
  mixins: [DeepForm],
  components: { ResetAndSave },
  formDefinition: {
    name: null,
    soa: SoaForm
  },
  methods: {
    endsWithDot(s) {
      if (s && !s.endsWith(".")) return "Must end with a dot.";
    },
    submit(done) {
      this.$apollo
        .mutate({
          mutation: api.dns.zones.CREATE_ZONE,
          variables: { input: this.form },
          refetchQueries: [{ query: api.dns.zones.LIST_ZONES }]
        })
        .then(notify(`${this.form.name} created`))
        .then(r => {
          if (r.success) this.$emit("ok");
        })
        .finally(done);
    }
  }
};
</script>
