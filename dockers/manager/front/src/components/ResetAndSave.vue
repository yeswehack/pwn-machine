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

    <div v-if="steps" class="col col-auto q-gutter-sm">
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
        :disabled="!isLastStep"
        :loading="isRunning"
        title="Save"
        :color="saveColor"
        icon="eva-save"
        @click="save"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
    step: { type: String, default: null },
    steps: { type: Array, default: null },
    validate: { type: Function, default: null },
    modified: { type: Boolean, default: false }
  },
  data: () => ({ isRunning: false }),
  computed: {
    stepIndex() {
      return this.steps?.findIndex(step => (step?.name ?? step) === this.step);
    },
    currentStep() {
      return this.steps?.find(step => (step?.name ?? step) === this.step);
    },
    firstStep() {
      return this.steps?.[0];
    },
    lastStep() {
      return this.steps?.[this.steps.length - 1];
    },
    isFirstStep() {
      return this.currentStep === this.firstStep;
    },
    isLastStep() {
      return this.currentStep === this.lastStep;
    },
    isValidStep() {
      return this.currentStep?.validate?.() ?? true;
    },
    saveColor() {
      return this.isLastStep ? "positive" : "grey";
    },
    resetColor() {
      return this.modified ? "primary" : "grey";
    }
  },
  methods: {
    emitStep(step) {
      this.$emit("update:step", step?.name ?? step);
    },
    save() {
      if (this.isValidStep) {
        this.isRunning = true;
        this.$emit("save", () => {
          this.isRunning = false;
        });
      }
    },
    reset() {
      this.emitStep(this.firstStep);
      this.$emit("reset");
      this.$nextTick(() => this.isValidStep);
    },
    nextStep() {
      if (this.isValidStep) {
        this.emitStep(this.steps[this.stepIndex + 1]);
      }
    },
    previousStep() {
      this.emitStep(this.steps[this.stepIndex - 1]);
    }
  }
};
</script>
