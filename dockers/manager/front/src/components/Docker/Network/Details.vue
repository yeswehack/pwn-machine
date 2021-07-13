<template>
  <div class="row q-gutter-md q-py-md">
    <div class="col">
      <q-card>
        <create-network :value="network" readonly />
      </q-card>
    </div>
    <div class="col">
      <q-card>
        <q-card-section class="q-pb-none">
          <div class="text-h6">Connect a container</div>
        </q-card-section>
        <q-card-section>
          <connect-container-input :network="network" />
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import CreateNetwork from "./Create.vue";
import ConnectContainerInput from "../ConnectContainerInput.vue";

export default {
  components: { CreateNetwork, ConnectContainerInput },
  props: {
    network: { type: Object, required: true }
  },
};
</script>
