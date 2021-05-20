<template>
  <div class="q-mb-md">
    <div class="row text-h6">{{ title }}</div>
    <div class="row q-gutter-sm">
      <q-select
        class="col"
        flat
        v-model="model"
        :options="containersNotAlreadyConnected"
        @input="addEntry"
        label="Connect a container"
      />
    </div>
    <q-list separator dense padding>
      <q-item :key="idx" v-for="(entry, idx) of form">
        <q-item-section>
          <div class="row q-col-gutter-sm">
            <div class="col">
              <container-link :name="entry.name" />
            </div>
            <div class="col col-auto">
              <q-btn
                flat
                dense
                icon="eva-close"
                color="negative"
                size="sm"
                @click="removeEntry(idx, entry)"
              />
            </div>
          </div>
        </q-item-section>
      </q-item>
      <q-item v-if="form.length == 0">
        <q-item-section>
          ...
        </q-item-section>
      </q-item>
    </q-list>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ContainerLink from "src/components/Docker/Container/Link.vue";
import api from "src/api";

export default {
  components: { ContainerLink },
  mixins: [DeepForm],
  props: {
    title: { type: String, default: "Containers" },
    label: { type: String, default: null }
  },
  apollo: {
    containers: {
      query: api.docker.GET_CONTAINERS,
      variables: { onlyRunning: true },
      update: data => data.dockerContainers
    }
  },
  data() {
    return { model: null };
  },
  formDefinition: [],
  computed: {
    containersNotAlreadyConnected() {
      return (this.containers || []).map(c => ({
        label: c.name,
        container: c,
        disable: !!this.form.find(x => x.name == c.name)
      }));
    }
  },
  methods: {
    addEntry() {
      if (!this.model) return;
      const container = this.model.container;
      this.form.unshift({ id: container.id, name: container.name });
      this.$emit("add", container.id);
      this.model = null;
    },
    removeEntry(idx, entry) {
      this.form.splice(idx, 1);
      this.$emit("remove", entry.id);
    }
  }
};
</script>
