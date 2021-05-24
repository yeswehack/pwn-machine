<template>
  <q-select
    ref="select"
    v-bind="$attrs"
    :options="imageOptions"
    v-model="form"
    input-debounce="0"
    label="Image"
    use-input
    fill-input
    :readonly="readonly"
    new-value-mode="add"
    hide-selected
    clearable
  >
    <template #append>
      <q-btn flat round icon="travel_explore" @click.stop="searchImage" v-if="!readonly" />
    </template>
  </q-select>
</template>

<script>
import api from "src/api";
import ImageSearchVue from "./ImageSearch.vue";
import DeepForm from "src/mixins/DeepForm";
export default {
  props: { readonly: { type: Boolean, default: false } },
  mixins: [DeepForm],
  formDefinition: null,
  apollo: {
    images: {
      query: api.docker.images.LIST_IMAGES,
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
          this.form = tag;
        });
    }
  }
};
</script>
