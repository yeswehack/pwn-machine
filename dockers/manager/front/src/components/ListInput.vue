<template>
  <base-grid-input
    v-bind="$attrs"
    :entries="form"
    :readonly="readonly"
    :grid-format="gridFormat"
    @addEntry="addEntry"
    @removeEntry="removeEntry"
  >
    <template #inputs>
      <div v-for="key of cols" :key="key" class="fit">
        <slot :name="key" :model="model" lazy-rules="ondemand" />
      </div>
    </template>

    <template #entry="{entry}">
      <div v-for="key of cols" :key="key" class="ellipsis">
        {{ entry[key] || "&ZeroWidthSpace;" }}

        <q-popup-edit v-model="entry[key]">
          <q-form greedy @keyup.enter="onenter" @submit="submit">
            <slot
              :name="key"
              :model="entry"
              :readonly="readonly"
              dense
              autofocus
            />
          </q-form>
        </q-popup-edit>
      </div>
    </template>
  </base-grid-input>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: { BaseGridInput },
  mixins: [DeepForm],
  formDefinition: [],
  props: {
    readonly: { type: Boolean, default: false },
    default: { type: Object, default: () => ({}) }
  },
  data() {
    return { model: { ...this.default }, onenter: null };
  },
  computed: {
    cols() {
      return Object.keys(this.$scopedSlots);
    },
    emptyModel() {
      return Object.fromEntries(this.cols.map(col => [col, null]));
    },
    gridFormat() {
      return "1fr ".repeat(this.cols.length);
    }
  },
  methods: {
    addEntry() {
      this.form.unshift({ ...this.emptyModel, ...this.model });
      this.model = { ...this.default };
    },
    removeEntry(i) {
      this.form.splice(i, 1);
    },
    submit() {
      this.onenter = () => {
        this.onenter = e => e.stopPropagation();
      };
    }
  }
};
</script>
