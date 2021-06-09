<template>
  <div class="q-gutter-md q-py-sm">
    <div class="row ">
      <div class="col q-mr-md">
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
            <reset-and-save
              :modified="modified"
              @reset="reset"
              @save="submit"
            />
          </q-card-section>
        </q-card>
      </div>
      <div class="col">
        <log-card>
          <log-list
            short
            flat
            :domain="`*${value.name.slice(0, -1)}`"
            type="*"
          />
        </log-card>
      </div>
    </div>
  </div>
</template>
<script>
import HelpLink from "src/components/HelpLink.vue";
import SoaForm from "./SoaForm.vue";
import LogList from "src/components/DNS/Log/LogList.vue";
import api from "src/api";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";
import LogCard from "src/components/LogCard.vue";

export default {
  components: { HelpLink, SoaForm, LogList, ResetAndSave, LogCard },
  mixins: [DeepForm],
  formDefinition: {
    soa: SoaForm
  },
  methods: {
    submit(done) {
      this.mutate({
        mutation: api.dns.zones.UPDATE_ZONE,
        variables: {
          nodeId: this.value.nodeId,
          patch: { soa: this.form.soa }
        },
        refetchQueries: [{ query: api.dns.zones.LIST_ZONES }],
        message: `${this.value.name} updated.`
      }).finally(done);
    }
  }
};
</script>
