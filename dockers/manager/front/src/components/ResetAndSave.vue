<template>
  <div class="col col-12 row q-py-sm justify-end">
    <div class="col col-auto q-gutter-md">
      <q-btn
        v-bind="$attrs"
        title="Reset"
        :color="resetColor"
        :disable="!modified"
        icon="eva-undo"
        @click="$emit('reset')"
      />
      <q-btn
        v-bind="$attrs"
        title="Save"
        :color="saveColor"
        :disable="!modified"
        icon="eva-save"
        @click="$emit('save')"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modified: { type: Boolean, default: false }
  },
  computed: {
    saveColor() {
      return this.modified ? "positive" : "grey";
    },
    resetColor() {
      return this.modified ? "primary" : "grey";
    }
  }
};
</script>

<style></style>
