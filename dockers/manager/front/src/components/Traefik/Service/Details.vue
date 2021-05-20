<template>
  <base-details :errors="value.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section class="row q-gutter-sm items-center">
            <div class="col col-auto">
              <protocol-badge :protocol="value.protocol" />
            </div>
            <div class="text-h6 col">
              {{ value.name }}
            </div>
            <div class="col col-auto">
              {{ value.type }}
            </div>
          </q-card-section>
          <q-card-section v-if="value.type!='internal' ">
            <component :is="createComponent" v-model="form.extra" />
          </q-card-section>
          <q-card-section v-if="value.type!='internal' ">
            <reset-and-save
              :modified="modified"
              @save="submit"
              @reset="reset"
            />
          </q-card-section>
        </q-card>
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

export default {
  mixins: [DeepForm],
  components: {
    BaseDetails,
    ProtocolBadge,
    ResetAndSave
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
      this.$apollo.mutate({

      })
    }
  }
};
</script>
