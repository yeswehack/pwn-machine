<template>
  <q-select
    v-bind="$attrs"
    :options="options"
    v-model="formData"
    @filter="filterOptions"
    input-debounce="0"
    label="Container"
    use-input
    dense
    filled
    fill-input
    hide-selected
    clearable
  />
</template>

<script>
import DeepForm from "src/mixins/DeepForm.js";
export default {
  mixins: [DeepForm],
  props: {
    allowNew: {
      type: Boolean,
      default: false
    },
    filter: {
      type: Function,
      default: () => true
    }
  },
  data() {
    const options = [];
    return { options };
  },
  computed: {
    containerNames() {
      return this.$store.getters["docker/containers"]
        .filter(this.filter)
        .map(container => container.Name);
    }
  },
  methods: {
    filterOptions(val, update) {
      update(() => {
        let options = this.allowNew ? ["New container"] : [];
        if (val === "") {
          options.push(...this.containerNames);
        } else {
          const needle = val.toLowerCase();
          options.push(
            ...this.containerNames.filter(
              v => v.toLowerCase().indexOf(needle) > -1
            )
          );
        }
        this.options = options;
      });
    }
  }
};
</script>
