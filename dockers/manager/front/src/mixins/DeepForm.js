import Vue from "vue";
import _ from "lodash";

function cleanTypename(o) {
  const cleaner = (key, value) => (key === "__typename" ? undefined : value);
  return JSON.parse(JSON.stringify(o), cleaner);
}

function isDeepForm(obj) {
  if (obj === null) {
    return false;
  }
  if (typeof obj !== "object") {
    return false;
  }
  return "formDefinition" in obj;
}

export function mapGetters(...names) {
  const getters = {};
  for (const name of names) {
    const parts = name.split(".");
    const fullName = name.replace(/\./g, "_");
    getters[fullName] = function() {
      return parts.reduce(
        (target, part) => target && target[part],
        this.form ?? {}
      );
    };
  }
  return getters;
}

export function required(msg) {
  return v => v && v != false || msg;
}

function isBasicType(obj) {
  return obj === null || ["number", "string", "boolean"].includes(typeof obj);
}

export default {
  props: { value: { default: null } },
  isDeepForm: true,
  data: () => ({
    form: {},
    originalForm: {},
    formChildren: {},
    internalEdit: false
  }),
  created() {
    this.buildOriginalForm();
    this.reset();
  },
  methods: {
    renderForm: f => f,
    required,
    validate: () => true,
    reset() {
      this.form = _.cloneDeep(this.originalForm);
    },
    submit() {
      this.$emit("submit", this.form);
    },
    instanciateSubForm(sub, value) {
      const ComponentClass = Vue.extend(sub);
      return new ComponentClass({ propsData: { value } });
    },
    buildOriginalForm() {
      const definition = this.$options.formDefinition;
      const value = this.value;
      if (isBasicType(definition)) {
        this.originalForm = value ?? definition;
      } else if (Array.isArray(definition)) {
        this.originalForm = value ? [...value] : [...definition];
      } else if (isDeepForm(definition)) {
        this.formChildren = definition;
        this.originalForm = this.instanciateSubForm(
          definition,
          value
        ).originalForm;
      } else {
        const originalForm = {};
        for (let [name, defaultValue] of Object.entries(definition)) {
          if (typeof defaultValue == "function") {
            defaultValue = defaultValue(value);
          }
          if (isDeepForm(defaultValue)) {
            this.formChildren[name] = defaultValue;
            originalForm[name] = this.instanciateSubForm(
              defaultValue,
              value?.[name]
            ).originalForm;
          } else {
            originalForm[name] = value?.[name] ?? defaultValue;
          }
        }
        this.originalForm = cleanTypename(originalForm);
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
