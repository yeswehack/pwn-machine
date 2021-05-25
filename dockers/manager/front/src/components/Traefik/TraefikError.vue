<template>
  <q-card class="bg-red-9 border-negative">
    <q-card-section>
      <div class="text-h6 q-pl-sm">
        {{ errors.length > 1 ? "Errors" : "Error" }}
      </div>
      <ul class="error-list">
        <li :key="idx" v-for="[idx, error] in errors.entries()">
          {{ error }}
        </li>
      </ul>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: {
    errors: Array
  }
};
</script>
<style lang="scss" scoped>
.error-list {
  padding-left: 20px;
}
</style>
