<template>
  <q-select
    ref="select"
    v-bind="$attrs"
    v-model="form"
    :options="imageOptions"
    input-debounce="0"
    label="Image"
    use-input
    emit-value
    :rules="[required('Image is required')]"
    map-options
    :readonly="readonly"
    clearable
    @filter="filterFn"
  >
    <template #after>
      <q-btn
        v-if="!readonly"
        round
        icon="eva-plus"
        color="positive"
        @click.stop="searchImage"
      />
    </template>
  </q-select>
</template>

<script>
import api from "src/api";
import ImageDialog from "../../Image/Dialog.vue";
import DeepForm from "src/mixins/DeepForm";

export default {
  mixins: [DeepForm],
  props: {
    readonly: { type: Boolean, default: false }
  },
  formDefinition: null,
  data: () => ({ filter: null }),
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
    update(v) {
      this.$emit("input", v?.value ?? null);
    },
    validate() {
      return this.$refs.select.validate();
    },
    searchImage() {
      const dialog = this.$q
        .dialog({
          component: ImageDialog,
          parent: this,
          input: this.filter,
        })
        .onOk(tag => {
          dialog.hide()
          this.$refs.select.add(tag);
          this.$refs.select.blur();
          this.form = tag;
        });
    }
  }
};
</script>
