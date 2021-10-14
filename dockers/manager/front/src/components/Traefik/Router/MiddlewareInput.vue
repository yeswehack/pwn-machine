<template>
  <div class="column">
    <q-select
      v-model="model"
      label="Middlewares"
      flat
      v-bind="$attrs"
      :options="options"
      @input="addEntry"
    >
      <template #after>
        <q-btn
          round
          dense
          size="md"
          color="green"
          icon="eva-plus"
          @click="createMiddleware"
        />
      </template>
    </q-select>
    <q-list separator dense padding class="drop-container">
      <div
        v-show="dragging"
        class="drop-zone"
        @drop="onDrop($event, 0)"
        @dragover.prevent
        @dragleave="dragLeave"
        @dragenter="dragEnter"
      />
      <template v-for="(entry, idx) of form">
        <q-item
          :key="idx"
          draggable
          @dragstart="dragStart($event, idx)"
          @dragend="dragEnd"
        >
          <q-item-section side>
            {{ idx + 1 }}
          </q-item-section>
          <q-item-section>
            {{ entry }}
          </q-item-section>
          <q-item-section avatar>
            <q-btn
              flat
              dense
              size="sm"
              color="negative"
              icon="eva-close"
              @click="removeEntry(idx)"
            />
          </q-item-section>
        </q-item>
        <div
          v-show="dragging"
          :key="`after-${idx}`"
          class="drop-zone"
          @drop="onDrop($event, idx + 1)"
          @dragover.prevent
          @dragleave="dragLeave"
          @dragenter="dragEnter"
        />
      </template>
      <q-item v-if="form.length === 0" class="empty">
        <q-item-section>...</q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import api from "src/api";
import MiddlewareDialog from "../Middleware/Dialog.vue";

function array_move(arr, from, to) {
  arr.splice(to, 0, arr.splice(from, 1)[0]);
}

export default {
  mixins: [DeepForm],
  formDefinition: [],
  apollo: {
    middlewares: {
      query: api.traefik.middlewares.LIST_MIDDLEWARES,
      update: data => data.traefikMiddlewares
    }
  },
  props: {
    label: { type: String, default: null }
  },
  data: () => ({ model: "", dragging: false }),
  computed: {
    options() {
      return (this.middlewares ?? []).map(m => m.name);
    }
  },
  methods: {
    createMiddleware() {
      this.$q.dialog({
        component: MiddlewareDialog,
        root: this
      });
    },
    addEntry() {
      if (!this.model) {
        return;
      }
      this.form.push(this.model);
      this.model = null;
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    },
    dragEnter(ev) {
      ev.target.classList.add("drag-over");
    },
    dragLeave(ev) {
      ev.target.classList.remove("drag-over");
    },
    onDrop(evt, newId) {
      const oldId = parseInt(evt.dataTransfer.getData("oldId"));
      if (newId !== oldId && newId !== oldId + 1) {
        array_move(this.form, oldId, newId);
      }
    },
    dragStart(evt, idx) {
      this.dragging = true;
      evt.dataTransfer.dropEffect = "move";
      evt.dataTransfer.effectAllowed = "move";
      evt.dataTransfer.setData("oldId", idx);
    },
    dragEnd() {
      for (const el of document.querySelectorAll(".drag-over")) {
        el.classList.remove("drag-over");
      }
      this.dragging = false;
    }
  }
};
</script>

<style lang="scss" scoped>
.drop-container {
  position: relative;
}
.q-item:not(.empty) {
  cursor: grab;
  &:hover {
    box-shadow: 0 0 1px 0 rgba(255, 255, 255, 0.4);
    border-radius: 4px;
  }
}
.drag-over + .q-item {
  margin-top: 10px;
}
.drop-zone {
  position: absolute;
  z-index: 1;
  height: 32px;
  width: 100%;
  transform: translateY(-50%);

  &.drag-over {
    box-shadow: 0 0 1px 0 rgba(255, 255, 255, 0.4);
    border-radius: 4px;
  }
}
</style>
