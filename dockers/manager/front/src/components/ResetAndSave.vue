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
  computed: {
    stepIndex() {
      if (!this.steps) return 0;
      return this.steps.findIndex(step =>
        typeof step == "string" ? step == this.step : step.name == this.step
      );
    },
    currentStep() {
      if (!this.steps) return null;
      return this.steps.find(step =>
        typeof step == "string" ? step == this.step : step.name == this.step
      );
    },
    firstStep() {
      return this.steps ? this.steps[0] : null;
    },
    lastStep() {
      return this.steps ? this.steps[this.steps.length - 1] : null;
    },
    isFirstStep() {
      return this.currentStep == this.firstStep;
    },
    isLastStep() {
      return this.currentStep == this.lastStep;
    },
    saveColor() {
      return this.isLastStep ? "positive" : "grey";
    },
    resetColor() {
      return this.modified ? "primary" : "grey";
    }
  },
  data() {
    return { isRunning: false };
    validate;
  },
  methods: {
    emitStep(step) {
      if (step == null || typeof step == "string") {
        this.$emit("update:step", step);
      } else {
        this.$emit("update:step", step.name);
      }
    },
    validateStep(step) {
      if (step == null) {
        return this.validate ? this.validate() : true;
      }
      if (typeof step == "string") {
        return true;
      } else {
        return step.validate ? step.validate() : true;
      }
    },
    save() {
      if (this.validateStep(this.currentStep)) {
        this.isRunning = true;
        this.$emit("save", () => {
          this.isRunning = false;
        });
      }
    },
    reset() {
      this.emitStep(this.firstStep);
      this.$emit("reset");
      this.$nextTick(() => {
        this.validateStep(this.currentStep);
      });
    },
    nextStep() {
      if (this.validateStep(this.currentStep)) {
        this.emitStep(this.steps[this.stepIndex + 1]);
      }
    },
    previousStep() {
      this.emitStep(this.steps[this.stepIndex - 1]);
    }
  }
};
</script>

<style></style>
