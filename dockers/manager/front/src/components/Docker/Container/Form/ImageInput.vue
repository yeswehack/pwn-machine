<template>
  <q-select
    ref="select"
    v-bind="$attrs"
    :options="imageOptions"
    v-model="form"
    input-debounce="0"
    label="Image"
    use-input
    emit-value
    :rules="[notEmpty]"
    map-options
    @filter="filterFn"
    :readonly="readonly"
    clearable
  >
    <template #append>
      <q-btn
        flat
        round
        icon="eva-plus"
        color="positive"
        @click.stop="searchImage"
        v-if="!readonly"
      />
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
  data() {
    return { filter: null };
  },
  apollo: {
    images: {
      query: api.docker.images.LIST_IMAGES,
      update: data => data.dockerImages
    }
  },
  computed: {
    imageOptions() {
      return (this.images ?? [])
        .map(image => image.name)
        .filter(i => i.toLowerCase().includes(this.filter ?? ""));
    }
  },
  methods: {
    filterFn(val, update) {
      this.filter = val.toLowerCase();
      update();
    },
    notEmpty(v) {
      if (!v) {
        return "Image is required";
      }
    },
    update(v) {
      this.$emit("input", v?.value ?? null);
    },
    validate() {
      return this.$refs.select.validate();
    },
    searchImage() {
      this.$q
        .dialog({
          component: ImageSearchVue,
          parent: this,
          input: this.filter,
          chooseImage: true
        })
        .onOk(tag => {
          this.$refs.select.add(tag);
          this.$refs.select.blur();
          this.form = tag;
        });
    }
  }
};
</script>
