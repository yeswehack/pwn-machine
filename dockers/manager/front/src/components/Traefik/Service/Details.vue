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
          <q-card-section v-if="value.type != 'internal'">
            <component :is="createComponent" v-model="form.extra" />
          </q-card-section>
          <q-card-section v-if="value.type != 'internal'">
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
          <log-list flat :service="[value.name]" short />
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
import LogCard from 'src/components/LogCard.vue';

export default {
  mixins: [DeepForm],
  components: {
    BaseDetails,
    ProtocolBadge,
    ResetAndSave,
    LogList,
    LogCard
  },
  formDefinition: {
    extra(value) {
      return getCreateComponent(value);
    }
  },
  computed: {
    createComponent() {
      return getCreateComponent(this.service);
    }
  },
  methods: {
    submit() {
      this.$apollo.mutate({});
    }
  }
};
</script>
