<template>
  <base-details :errors="value.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section>
            <div class="row q-gutter-sm items-center">
              <div class="col col-auto">
                <protocol-badge :protocol="value.protocol" />
              </div>
              <div class="text-h6 col">
                {{ value.name }}
              </div>
              <div class="col col-auto">
                {{ value.type }}
              </div>
            </div>
          </q-card-section>
          <q-card-section v-if="value.type !== 'internal'">
            <component :is="formChildren.extra" v-model="form.extra" />
          </q-card-section>
          <q-card-section v-if="value.type !== 'internal'">
            <reset-and-save
              :modified="modified"
              @save="submit"
              @reset="reset"
            />
          </q-card-section>
        </q-card>
      </div>

      <div class="col col-6">
        <log-card>
          <log-list flat short :service="[value.name]" />
        </log-card>
      </div>
    </template>
  </base-details>
</template>

<script>
import { getCreateComponent } from "./Create.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
import ProtocolBadge from "../ProtocolBadge.vue";
import DeepForm from "src/mixins/DeepForm";
import ResetAndSave from "src/components/ResetAndSave.vue";
import LogList from "src/components/Traefik/Log/LogList.vue";
import LogCard from "src/components/LogCard.vue";

export default {
  components: {
    BaseDetails,
    ProtocolBadge,
    ResetAndSave,
    LogList,
    LogCard
  },
  mixins: [DeepForm],
  formDefinition: {
    extra: getCreateComponent
  }
};
</script>
