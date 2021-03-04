<template>
  <q-select
    v-bind="$attrs"
    :options="options"
    v-model="formData"
    @filter="filterOptions"
    input-debounce="0"
    label="Image"
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
    imageNames() {
      return this.$store.getters["docker/images"]
        .filter(this.filter)
        .map(image => `${image.Repository}:${image.Tag}`);
    }
  },
  methods: {
    filterOptions(val, update) {
      update(() => {
        if (val === "") {
          this.options = this.imageNames;
        } else {
          const needle = val.toLowerCase();
          this.options = this.imageNames.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          );
        }
      });
    }
  }
};
</script>
