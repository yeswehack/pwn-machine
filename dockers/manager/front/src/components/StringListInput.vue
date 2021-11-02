<template>
  <div class="">
    <div class="row items-center">
      <div class="col q-mr-md">
        <q-input v-model="model" :label="label" @keydown.enter="addEntry" />
      </div>
      <div class="col col-auto">
        <q-btn
          dense
          round
          flat
          size="md"
          icon="eva-plus"
          color="positive"
          @click="addEntry"
        />
      </div>
    </div>
    <div v-for="(entry, key) of form" :key="key">
      <div v-if="key > 0" class="separator"></div>
      <div class="row q-py-sm items-center">
        <div class="col">
          {{ entry }}
          <q-popup-edit
            v-model="entry[key]"
            auto-save
            @save="save(entry, key, arguments[1])"
          >
            <q-form :ref="key" greedy @submit.stop>
              <q-input v-model="form[key]" />
            </q-form>
          </q-popup-edit>
        </div>
        <div class="col col-auto">
          <q-btn
            dense
            round
            flat
            icon="eva-close"
            color="negative"
            @click="removeEntry(key)"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import BaseGridInput from "src/components/BaseGridInput.vue";

export default {
  components: {},
  mixins: [DeepForm],
  formDefinition: [],
  props: {
    readonly: { type: Boolean, default: false },
    default: { type: String, default: "" },
    label: {type: String, default: ""}
  },
  data() {
    return { model: this.default };
  },
  computed: {
    cols() {
      return Object.keys(this.$scopedSlots)
        .filter(slot => !slot.startsWith("display-"))
        .map(slot => {
          const [key, ...mods] = slot.split(".");
          return { slot, key: "v", mods };
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
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    addEntry() {
      this.form.unshift(this.model);
      this.model = this.default;
    },
    async save(entry, key, oldValue) {
      const valid = await this.$refs[key][0].validate();
      if (!valid) entry[key] = oldValue;
    },
  }
};
</script>

<style scoped>
.separator {
  background: rgba(255, 255, 255, 0.28);
  height: 1px;
  width: 100%;
  justify-self: center;
}
</style>
