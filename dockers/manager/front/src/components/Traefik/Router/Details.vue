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
          <component :is="formChildren.extra" v-model="form.extra" />
          <q-card-section>
            <reset-and-save
              :modified="modified"
              @save="submit"
              @reset="reset"
            />
          </q-card-section>
        </q-card>
      </div>
      <div class="col col-6">
        <middleware-list :middlewares.sync="form.middlewares" v-if="0" />
      </div>
    </template>
  </base-details>
</template>

<script>
import MiddlewareList from "src/components/Traefik/Router/MiddlewareList.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
import DeepForm from "src/mixins/DeepForm";
import { getCreateComponent } from "./Create.vue";
import ResetAndSave from "src/components/ResetAndSave.vue";
import ProtocolBadge from "../ProtocolBadge.vue";
import api from "src/api";

export default {
  components: { MiddlewareList, ProtocolBadge, BaseDetails, ResetAndSave },
  mixins: [DeepForm],
  formDefinition: {
    extra(value) {
      return getCreateComponent(value);
    }
  },
  methods: {
    submit(done) {
      this.$apollo
        .mutate({
          mutation: api.traefik.UPDATE_ROUTER[this.value.protocol],
          variables: { id: this.value.nodeId, patch: this.form.extra },
          refetchQueries: [{ query: api.traefik.GET_ROUTERS }]
        })
        .then(done);
    }
  }
};
</script>
