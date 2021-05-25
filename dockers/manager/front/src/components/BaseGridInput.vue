<template>
  <div>
    <div class="input-grid" :style="style">
      <template v-if="readonly">
        <div
          class="text-bold"
          :key="`title-${idx}`"
          v-for="(title, idx) of titles"
        >
          {{ title }}
        </div>
      </template>
      <template v-else>
        <slot name="inputs" />
        <div class="text-center" v-if="!readonly">
          <q-btn
            dense
            round
            flat
            size="md"
            icon="eva-plus"
            color="positive"
            @click="$emit('addEntry')"
          />
        </div>
      </template>
      <div class="spacing" v-if="!readonly"></div>
      <div :key="idx" v-for="(entry, idx) of entries" style="display: contents">
        <div class="separator" v-if="idx > 0"></div>
        <slot name="entry" :entry="entry" />
        <div class="text-center" v-if="!readonly">
          <q-btn
            dense
            round
            flat
            icon="eva-close"
            color="negative"
            @click="$emit('removeEntry', idx)"
          />
        </div>
      </div>
    </div>
    <label class="row text-negative" v-if="error">{{ error }}</label>
  </div>
</template>

<script>
export default {
  props: {
    readonly: { type: Boolean, default: false },
    titles: { type: Array, default: () => [] },
    entries: { type: Array, default: () => [] },
    gridFormat: { type: String, default: "" },
    error: { type: String, default: null }
  },
  computed: {
    style() {
      const columnEnd = this.gridFormat.split(/\s+/).length + 1;
      if (this.readonly) {
        return {
          "grid-template-columns": this.gridFormat,
          "--column-end": columnEnd
        };
      }
      return {
        "grid-template-columns": this.gridFormat + " 34px",
        "--column-end": columnEnd + 1
      };
    }
  }
};
</script>
<style lang="scss" scoped>
.input-grid {
  width: 100%;
  display: grid;
  align-items: center;
  row-gap: 4px;
  column-gap: 10px;
}
.spacing,
.separator {
  grid-column-start: 1;
  grid-column-end: var(--column-end);
}

.spacing {
  height: 8px;
}

.separator {
  background: rgba(255, 255, 255, 0.28);
  height: 1px;
  width: calc(100% + 12px);
  justify-self: center;
}
</style>
