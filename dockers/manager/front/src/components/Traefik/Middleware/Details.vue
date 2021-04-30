<template>
  <BaseDetails :errors="middleware.error">
    <template #body>
      <div class="col col-6">
        <q-card>
          <q-card-section class="text-h6">
            {{ middleware.name }}
          </q-card-section>
          <create-middleware edit :middleware="middleware" />
        </q-card>
      </div>
      <div class="col col-6"></div>
    </template>
  </BaseDetails>
</template>

<script>
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
export default {
  components: { CreateMiddleware, BaseDetails },
  props: {
    middleware: { type: Object, required: true }
  }
};
</script>
