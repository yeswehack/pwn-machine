<template>
  <base-dialog
    ref="dialog"
    :width="800"
    title="Create a new image"
    help="https://docs.docker.com/engine/reference/commandline/container_create/"
  >
    <template #default>
      <q-tabs v-model="tab" class="q-mx-md q-mt-sm">
        <q-tab label="From dockerhub" name="search" />
        <q-tab label="From git/url" name="url" />
        <q-space />
      </q-tabs>
      <q-tab-panels v-model="tab" animated>
        <q-tab-panel name="search">
          <image-from-hub
            @ok="(name) => $emit('ok', name)"
          />
        </q-tab-panel>
        <q-tab-panel name="url">
          <image-from-url
            @ok="(name) => $emit('ok', name)"
          />
        </q-tab-panel>
      </q-tab-panels>
    </template>
  </base-dialog>
</template>

<script>
import BaseDialog from "src/components/BaseDialog.vue";
import ImageFromHub from './FromDockerHub.vue';
import ImageFromUrl from './FromUrl.vue';

export default {
  components: { BaseDialog, ImageFromHub, ImageFromUrl },
  data: () => ({ tab: "search" }),
  methods: {
    show () {
      this.$refs.dialog.show();
    },
    hide () {
      this.$refs.dialog.hide();
    }
  }
};
</script>
