import deepEqual from "deep-equal";
import deepcopy from "deepcopy";

export default {
  props: {
    value: { default: null }
  },
  data() {
    const originalForm = this.createDefaultForm(this.value);
    const form = deepcopy(originalForm);
    return { form, originalForm, internalEdit: false };
  },
  methods: {
    createDefaultForm(value) {
      return value ? deepcopy(value) : {};
    },
    renderForm(f){
      return f
    },
    clear() {
      this.form = this.createDefaultForm();
    },
    reset() {
      this.form = deepcopy(this.originalForm);
    },
    submit() {
      this.$emit("submit", this.form);
    }
  },
  computed: {
    modified() {
      return !deepEqual(this.form, this.originalForm);
    }
  },
  watch: {
    value: {
      immediate: true,
      handler(value) {
        if (!this.internalEdit) {
          this.originalForm = this.createDefaultForm(value);
        }
      }
    },
    form: {
      deep: true,
      async handler() {
        this.internalEdit = true;
        await this.$emit("input", this.renderForm(this.form));
        this.internalEdit = false;
      }
    }
  }
};
