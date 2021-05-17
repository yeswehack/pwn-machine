<template>
  <div class="row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">{{ value.name }}</div>
            <q-space />
            <div title="Serial" class="text-mono">{{ value.serial }}</div>
            <help-link
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <component :is="formChildren.soa" v-model="form.soa" />
        </q-card-section>
        <q-card-section>
          <reset-and-save :modified="modified" @reset="reset" @save="submit" />
        </q-card-section>
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section>
          <div class="text-h6">Logs</div>
        </q-card-section>
        <q-card-section>
          <log-list flat :domain="`*${value.name}`" type="*" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>
<script>
import HelpLink from "src/components/HelpLink.vue";
import SoaForm from "./SoaForm.vue";
import LogList from "src/components/DNS/LogList.vue";
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";

export default {
  mixins: [DeepForm],
  components: { HelpLink, SoaForm, LogList, ResetAndSave },
  props: {
    zone: { type: Object, default: null }
  },
  formDefinition: {
    soa: SoaForm
  },
  methods: {
    submit() {
      this.$apollo.mutate({
        mutation: api.dns.UPDATE_ZONE,
        variables: { nodeId: this.value.nodeId, patch: { soa: this.form.soa } },
        refetchQueries: [{ query: api.dns.GET_ZONES }]
      });
    }
  }
};
</script>
