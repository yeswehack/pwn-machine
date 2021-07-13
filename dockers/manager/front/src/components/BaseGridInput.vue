<template>
  <div>
    <div class="input-grid" :style="style">
      <template v-if="readonly">
        <div
          v-for="(title, idx) of titles"
          :key="`title-${idx}`"
          class="text-bold"
        >
          {{ title }}
        </div>
      </template>
      <q-form
        v-else
        ref="form"
        style="display: contents"
        greedy
        @input="$refs.form.resetValidation()"
        @submit="$emit('addEntry')"
      >
        <slot name="inputs" />
        <div v-if="!readonly" class="text-center">
          <q-btn
            dense
            round
            flat
            size="md"
            icon="eva-plus"
            color="positive"
            :loading="loading"
            type="submit"
          />
        </div>
      </q-form>
      <div v-if="!readonly" class="spacing" />
      <div v-if="readonly && entries.length === 0" style="display: contents">
        <div v-for="(title, idx) of titles" :key="`title-${idx}`">-</div>
      </div>
      <div v-for="(entry, idx) of entries" :key="idx" style="display: contents">
        <div v-if="idx > 0" class="separator"></div>
        <slot name="entry" :entry="entry">
          <div class="ellipsis">{{ entry }}</div>
        </slot>
        <div v-if="!readonly" class="text-center">
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
    <label v-if="error" class="row text-negative">{{ error }}</label>
  </div>
</template>

<script>
export default {
  props: {
    loading: { type: Boolean, default: false },
    readonly: { type: Boolean, default: false },
    titles: { type: Array, default: () => [] },
    entries: { type: Array, default: () => [] },
    gridFormat: { type: String, default: "" },
    error: { type: String, default: null }
  },
  computed: {
    style() {
      const columnEnd = this.gridFormat.trim().split(/\s+/).length + 1;
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
