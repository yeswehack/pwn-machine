<template>
  <BaseDetails :errors="router.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section class="text-h6">
            {{ router.name }}
          </q-card-section>
          <create-router hide-name :value="extraForm(router)" />
        </q-card>
      </div>
      <div class="col col-6">
        <MiddlewareList :middlewares.sync="router.middlewares" v-if="0" />
      </div>
    </template>
  </BaseDetails>
</template>

<script>
import CreateRouter from "src/components/Traefik/Router/Create.vue";
import MiddlewareList from "src/components/Traefik/Router/MiddlewareList.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
export default {
  components: {
    CreateRouter,
    MiddlewareList,
    BaseDetails
  },
  props: {
    router: {
      type: Object,
      required: true
    }
  },
  data() {
    return {};
  },
  methods: {
    extraForm(f) {
      const extra = {
        rule: f.rule,
        priority: f.priority,
        entryPoints: (f.entryPoints ?? []).map(ep => ep.name),
        service: f.service?.name,
        middlewares: (f.middlewares ?? []).map(m => m.name)
      };

      return { ...f, extra };
    }
  }
};
</script>
