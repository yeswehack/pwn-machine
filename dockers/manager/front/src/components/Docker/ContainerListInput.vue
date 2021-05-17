<template>
  <div class="q-mb-md">
    <div class="row text-h6">{{ title }}</div>
    <div class="row q-gutter-sm">
      <q-select
        class="col"
        flat
        v-model="model.name"
        :options="containersNotAlreadyConnected"
        @keypress.enter.prevent="addEntry"
        label="Connect a container"
      >
        <template #append>
          <q-btn
            dense
            flat
            size="md"
            icon="eva-plus"
            color="positive"
            @click.stop="addEntry"
          />
        </template>
      </q-select>
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
                @click="removeEntry(idx)"
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
import gql from "src/api";

export default {
  components: { ContainerLink },
  mixins: [DeepForm],
  props: {
    title: { type: String, default: "Containers" },
    label: { type: String, default: null }
  },
  apollo: {
    containers: {
      query: gql.docker.GET_CONTAINERS,
      update: data => data.dockerContainers
    }
  },
  data() {
    return { model: { name: null } };
  },
  formDefinition: [],
  computed: {
    containersNotAlreadyConnected() {
      return (this.containers || []).map(c => ({
        label: c.name,
        value: c.id,
        disable: !!this.form.find(x => x.name == c.name)
      }));
    }
  },
  methods: {
    addEntry() {
      this.form.unshift({ name: this.model.name.label });
      this.model = { name: null };
    },
    removeEntry(idx) {
      this.form.splice(idx, 1);
    }
  }
};
</script>
