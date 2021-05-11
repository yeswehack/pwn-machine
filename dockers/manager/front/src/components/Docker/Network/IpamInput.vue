<template>
  <div>
    <q-input v-model="form.subnet" label="Subnet" />
    <q-input v-model="form.range" label="Range" />
    <q-input v-model="form.gateway" label="Gateway" />
  </div>
</template>

<script>
import DeepForm from 'src/mixins/DeepForm'
export default {
  mixins: [DeepForm],
  formDefinition: {
    subnet: null,
    range: null,
    gateway: null
  }
}
</script>

<style>

</style>