<template>
  <q-card class="create-router bg-dark">
    <q-card-section>
      <div class="row items-center q-gutter-md">
        <div class="text-h6">Middlewares</div>
        <div>
          <q-btn
            round
            size="sm"
            dense
            color="positive"
            icon="add"
            title="Create a new middleware"
            @click="createMiddlewareVisible = true"
          />
        </div>
      </div>
    </q-card-section>
    <q-card-section class="q-gutter-md">
      <div class="col-12" :key="idx" v-for="[idx] in middlewares.entries()">
        <div class="row justify-stretch items-center q-col-gutter-md">
          <div class="col-auto col-grow">
            <q-select
              fill-input
              v-model="middlewares[idx]"
              :options="middlewares.map(m => m.name)"
            />
          </div>
          <div class="col-auto">
            <q-btn
              round
              icon="delete"
              color="red"
              @click="deleteFromChain(idx)"
            />
          </div>
        </div>
      </div>
      <q-btn
        color="green"
        rounded
        icon="add"
        @click="addChainEntry"
        label="Add"
      />
    </q-card-section>
    <q-card-actions align="right" class="q-pa-md">
      <q-btn
        label="Reset"
        @click="reset"
        color="warning"
        flat
        class="q-py-xs q-px-md"
      />
      <q-btn color="positive" @click="save" class="q-py-xs q-px-md">
        Save
      </q-btn>
    </q-card-actions>
  </q-card>
</template>

<script>
export default {
  props: {
    middlewares: Array
  },
  data() {
    const form = {};
    return { form, createMiddlewareVisible: false };
  }
};
</script>

<style></style>
