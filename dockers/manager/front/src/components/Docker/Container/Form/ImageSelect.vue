<template>
  <q-select
    ref="select"
    v-bind="$attrs"
    :options="imageOptions"
    v-model="model"
    input-debounce="0"
    label="Image"
    use-input
    fill-input
    new-value-mode="add"
    hide-selected
    clearable
    @input="update"
  >
    <template #append>
      <q-btn flat round icon="travel_explore" @click.stop="searchImage" />
    </template>
  </q-select>
</template>

<script>
import gql from "src/gql";
import ImageSearchVue from "./ImageSearch.vue";
export default {
  props: {
    value: { type: String, default: null }
  },
  data() {
    return { model: null };
  },
  apollo: {
    images: {
      query: gql.docker.GET_IMAGES,
      update: data => data.dockerImages
    }
  },
  computed: {
    imageOptions() {
      return (this.images ?? []).map(image => ({
        label: image.name,
        value: image.id
      }));
    }
  },
  methods: {
    update(v) {
      this.$emit("input", v?.value ?? null);
    },
    searchImage() {
      this.$q
        .dialog({
          component: ImageSearchVue,
          parent: this
        })
        .onOk(tag => {
          this.$refs.select.add(tag);
          this.model = tag;
          this.$emit("input",tag);
        });
    }
  }
};
</script>
