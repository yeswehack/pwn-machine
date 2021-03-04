<template>
  <q-select
    v-bind="$attrs"
    :options="options"
    v-model="formData"
    @filter="filterOptions"
    input-debounce="0"
    label="Volume"
    use-input
    dense
    filled
    fill-input
    use-chips
    multiple
  >
    <template
      v-slot:option="{ itemProps, itemEvents, opt, selected, toggleOption }"
    >
      <q-item v-bind="itemProps" v-on="itemEvents">
        <q-item-section>
          <q-item-label>{{ opt }}</q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-toggle :value="selected" @input="toggleOption(opt)" />
        </q-item-section>
      </q-item>
    </template>
  </q-select>
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
    volumeNames() {
      return this.$store.getters["docker/volumes"]
        .filter(this.filter)
        .map(volume => `${volume.Name}`);
    }
  },
  methods: {
    filterOptions(val, update) {
      update(() => {
        if (val === "") {
          this.options = this.volumeNames;
        } else {
          const needle = val.toLowerCase();
          this.options = this.volumeNames.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          );
        }
      });
    }
  }
};
</script>
