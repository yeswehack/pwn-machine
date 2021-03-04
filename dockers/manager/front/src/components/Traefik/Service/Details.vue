<template>
  <BaseDetails :errors="service.error">
    <template #body>
      <div class="col col-auto">
        <CreateService
          class="bg-dark"
          edit
          v-on:created="serviceModified"
          :info="service"
          :services="services"
          :routers="routers"
          :entrypoints="entrypoints"
        />
      </div>
    </template>
  </BaseDetails>
</template>

<script>
import CreateService from "src/components/Traefik/Service/Create.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
export default {
  components: { CreateService, BaseDetails },
  props: {
    name: {
      type: String
    },
    services: {
      type: Array
    },
    routers: {
      type: Array
    },
    entrypoints: {
      type: Array
    },
    middlewares: {
      type: Array
    }
  },
  data() {
    return {
      service: this.services.find(r => r.name == this.name)
    };
  },
  methods: {
    serviceModified() {
      this.$emit("modified");
    }
  }
};
</script>
