
<template>
  <q-list separator class="rounded-borders" bordered>
    <q-expansion-item expand-separator icon="label" label="Source criterion">
      <q-separator />
      <q-card>
        <q-card-section>
        <div class="column q-gutter-sm">
      <component :is="formChildren.ipStrategy" v-model="form.ipStrategy" label="Ip strategy" />
      <q-input v-model="form.requestHeaderName" label="Request header name" />
      <q-toggle v-model="form.requestHost" label="Request host" />
</div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>
<script>
import DeepForm from "src/mixins/DeepForm";
import ipStrategy from './ipStrategy.vue';
export default {
    components: {  ipStrategy },
    mixins: [DeepForm],
    formDefinition: {
  ipStrategy: ipStrategy,
  requestHeaderName: null,
  requestHost: null,
},
}
</script>
