<template>
  <q-select
    ref="select"
    v-bind="$attrs"
    :options="options"
    v-model="formData"
    @filter="filterOptions"
    input-debounce="0"
    label="Network"
    use-input
    dense
    filled
    fill-input
    use-chips
    multiple
    @add="checkForConflict"
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
    networkNames() {
      return this.$store.getters["docker/networks"]
        .filter(this.filter)
        .map(network => `${network.Name}`);
    }
  },
  methods: {
    checkForConflict(opt) {
      if (["none", "host"].includes(opt.value)) {
        console.log("reset")
        this.$refs.select.reset()
        //this.$refs.select.add(opt.value)
      }
    },
    filterOptions(val, update) {
      update(() => {
        if (val === "") {
          this.options = this.networkNames;
        } else {
          const needle = val.toLowerCase();
          this.options = this.networkNames.filter(
            v => v.toLowerCase().indexOf(needle) > -1
          );
        }
      });
    }
  }
};
</script>
