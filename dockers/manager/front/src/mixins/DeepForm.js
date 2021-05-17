import Vue from "vue";
import _ from "lodash";

function isDeepForm(obj) {
  if (obj === null) {
    return false;
  }
  if (typeof obj !== "object") {
    return false;
  }
  return "formDefinition" in obj;
}

export default {
  props: {
    value: { default: null }
  },
  isDeepForm: true,
  data() {
    return {
      form: {},
      originalForm: {},
      formChildren: {},
      internalEdit: false
    };
  },
  created() {
    this.buildOriginalForm();
    this.reset();
  },
  methods: {
    renderForm(f) {
      return f;
    },
    reset() {
      this.form = _.cloneDeep(this.originalForm);
    },
    submit() {
      this.$emit("submit", this.form);
    },
    instanciateSubForm(sub, value) {
      const ComponentClass = Vue.extend(sub);
      const instance = new ComponentClass({
        propsData: { value: value }
      });
      instance.$mount();
      return instance;
    },
    buildOriginalForm() {
      const definition = this.$options.formDefinition;
      
      if (definition === null){
        this.originalForm = null
      }
      else if (Array.isArray(definition)) {
        this.originalForm = this.value ? [...this.value] : [...definition];
      } else {
        const originalForm = {};
        for (let [name, defaultValue] of Object.entries(definition)) {
          if (typeof defaultValue == "function") {
            defaultValue = defaultValue(this.value);
          }
          if (isDeepForm(defaultValue)) {
            this.formChildren[name] = defaultValue;
            originalForm[name] = this.instanciateSubForm(
              defaultValue,
              this.value?.[name]
            ).originalForm;
          } else {
            originalForm[name] = this.value?.[name] ?? defaultValue;
          }
        }
        this.originalForm = originalForm;
      }
    }
  },
  computed: {
    modified() {
      return !_.isEqual(this.form, this.originalForm);
    }
  },
  watch: {
    value() {
      if (!this.internalEdit) {
        this.buildOriginalForm();
        this.reset();
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
