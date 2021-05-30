<template>
  <div class="row justify-center full-width">
    <div class="col col-auto" style="width: 600px">
      <q-card bordered flat>
        <q-card-section>
          <div class="text-h6">Open a new shell</div>
        </q-card-section>
        <q-separator />
        <create-shell />
      </q-card>
    </div>
  </div>
</template>

<script>
import CreateShell from "./Create.vue";
export default {
  components: { CreateShell }
};
</script>

<style></style>
