<template>
  <base-details :errors="value.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section>
            <div class="row items-center">
              <div class="col text-h6">
                {{ value.name }}
              </div>
              <div class="col col-auto">
                <protocol-badge :protocol="value.protocol" />
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <component
              :is="formChildren.extra"
              ref="create"
              v-model="form.extra"
            />
          </q-card-section>
          <q-card-section>
            <reset-and-save
              :modified="modified"
              :validate="validate"
              @save="submit"
              @reset="reset"
            />
          </q-card-section>
        </q-card>
      </div>

      <div class="col col-6">
        <log-card>
          <log-list flat short :router="[value.name]" />
        </log-card>
      </div>
    </template>
  </base-details>
</template>

<script>
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
import DeepForm from "src/mixins/DeepForm";
import { getCreateComponent } from "./Create.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import ProtocolBadge from "../ProtocolBadge.vue";
import LogList from "src/components/Traefik/Log/LogList.vue";
import api from "src/api";
import LogCard from "src/components/LogCard.vue";

export default {
  components: {
    ProtocolBadge,
    BaseDetails,
    ResetAndSave,
    LogList,
    LogCard
  },
  mixins: [DeepForm],
  formDefinition: {
    extra: getCreateComponent
  },
  methods: {
    submit(done) {
      this.mutate({
        mutation: api.traefik.routers.UPDATE_ROUTER[this.value.protocol],
        variables: { id: this.value.nodeId, patch: this.form.extra },
        refetchQueries: [{ query: api.traefik.routers.LIST_ROUTERS }],
        message: `${this.value.name} updated.`
      }).finally(done);
    }
  }
};
</script>
