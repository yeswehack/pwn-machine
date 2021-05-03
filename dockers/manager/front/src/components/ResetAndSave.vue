<template>
  <div class="row justify-between">
    <div class="col col-auto">
      <q-btn
        title="Reset"
        :color="resetColor"
        :disable="!modified"
        icon="eva-undo"
        @click="reset"
      />
    </div>

    <div class="col col-auto q-gutter-sm" v-if="steps">
      <q-btn
        :disabled="isFirstStep"
        title="Back"
        color="positive"
        icon="eva-arrow-ios-back-outline"
        @click="previousStep"
      />
      <q-btn
        :disabled="isLastStep"
        title="Next"
        color="positive"
        icon="eva-arrow-ios-forward-outline"
        @click="nextStep"
      />
    </div>

    <div class="col col-auto">
      <q-btn
        :disabled="!modified || !isLastStep"
        title="Save"
        :color="saveColor"
        icon="eva-save"
        @click="$emit('save')"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    step: { type: String, default: null },
    steps: { type: Array, default: null },
    modified: { type: Boolean, default: false }
  },
  computed: {
    stepIndex() {
      return this.steps.indexOf(this.step);
    },
    firstStep() {
      return this.steps ? this.steps[0] : null;
    },
    lastStep() {
      return this.steps ? this.steps[this.steps.length - 1] : null;
    },
    isFirstStep() {
      return this.step == this.firstStep;
    },
    isLastStep() {
      return this.step == this.lastStep;
    },
    saveColor() {
      return this.modified && this.isLastStep ? "positive" : "grey";
    },
    resetColor() {
      return this.modified ? "primary" : "grey";
    }
  },
  methods: {
    reset() {
      this.$emit("update:step", this.firstStep);
      this.$emit("reset");
    },
    nextStep() {
      this.$emit("update:step", this.steps[this.stepIndex + 1]);
    },
    previousStep() {
      this.$emit("update:step", this.steps[this.stepIndex - 1]);
    }
  }
};
</script>

<style></style>
