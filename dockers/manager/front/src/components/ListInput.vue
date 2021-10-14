<template>
  <base-grid-input
    v-bind="$attrs"
    :entries="form"
    :readonly="readonly"
    @addEntry="addEntry"
    @removeEntry="form.splice($event, 1)"
  >
    <template #inputs>
      <template v-for="{ slot } of cols">
        <div v-if="!isEmpty(slot, model)" :key="slot" class="fit">
          <slot :name="slot" :model="model" lazy-rules="ondemand" />
        </div>
      </template>
    </template>

    <template #entry="{entry}">
      <template v-for="{ slot, key, mods } of cols">
        <div v-if="!isEmpty(slot, entry)" :key="key" class="ellipsis">
          <template v-if="!mods.includes('nopopup')">
            <slot :name="`display-${key}`" v-bind="entry">
              {{ entry[key] || "&ZeroWidthSpace;" }}
            </slot>

            <q-popup-edit
              v-if="!mods.includes('noedit')"
              v-model="entry[key]"
              auto-save
              @save="save(entry, key, arguments[1])"
            >
              <q-form :ref="key" greedy @submit.stop>
                <slot
                  :name="slot"
                  :model="entry"
                  :readonly="readonly"
                  dense
                  autofocus
                />
              </q-form>
            </q-popup-edit>
          </template>

          <template v-else>
            <slot :name="slot" :model="entry" :disable="readonly" dense />
          </template>
        </div>
      </template>
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
    return { model: { ...this.default } };
  },
  computed: {
    cols() {
      return Object.keys(this.$scopedSlots)
        .filter(slot => !slot.startsWith("display-"))
        .map(slot => {
          const [key, ...mods] = slot.split(".");
          return { slot, key, mods };
        });
    },
    emptyModel() {
      return Object.fromEntries(this.cols.map(({ key }) => [key, null]));
    }
  },
  methods: {
    isEmpty(slot, model) {
      return this.$scopedSlots[slot]({ model }) === undefined;
    },
    addEntry() {
      this.form.unshift({ ...this.emptyModel, ...this.model });
      this.model = { ...this.default };
    },
    async save(entry, key, oldValue) {
      const valid = await this.$refs[key][0].validate();
      if (!valid) entry[key] = oldValue;
    }
  }
};
</script>
