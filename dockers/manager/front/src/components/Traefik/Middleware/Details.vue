<template>
  <BaseDetails :errors="middleware.error">
    <template #body>
      <div class="col col-grow">
        <CreateMiddleware
          style="max-width: 100%"
          class="bg-dark"
          edit
          v-on:created="middlewareModified"
          :info="middleware"
        />
      </div>
    </template>
  </BaseDetails>
</template>

<script>
import CreateMiddleware from "src/components/Traefik/Middleware/Create.vue";
import BaseDetails from "src/components/Traefik/BaseDetails.vue";
export default {
  components: { CreateMiddleware, BaseDetails },
  props: {
    name: {
      type: String
    },
    middlewares: {
      type: Array
    }
  },
  data() {
    return {
      middleware: this.middlewares.find(r => r.name == this.name)
    };
  },
  methods: {
    middlewareModified() {
      this.$emit("modified");
    }
  }
};
</script>
