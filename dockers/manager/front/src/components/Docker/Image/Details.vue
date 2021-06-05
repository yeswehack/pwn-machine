<template>
  <div class="q-col-gutter-md row q-py-sm">
    <div class="col col-6">
      <q-card>
        <q-card-section>
          <div class="text-h6">
            Tags
          </div>
          <list-input v-model="image.tags" />
        </q-card-section>
      </q-card>
    </div>
    <div class="col col-6">
      <q-card style="max-width:100vw">
        <q-card-section class="text-h6">
          Image history
        </q-card-section>
        <q-card-section>
          <div class="text-h6">
            Tags
          </div>
          <q-table
            dense
            hide-bottom
            flat
            :data="image.history"
            :columns="columns"
            :rows-per-page-options="[0]"
          >
            <template #body-cell-operation="{value}">
              <q-td auto-width>
                {{ value }}
              </q-td>
            </template>
            <template #body-cell-argument="{value}">
              <q-td class="ellipsis" style="max-width:300px">
                {{ value }}
                <q-popup-edit>
                  <q-input readonly :value="value" autofocus />
                </q-popup-edit>
              </q-td>
            </template>
          </q-table>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script>
import ListInput from "src/components/ListInput.vue";

export default {
  components: { ListInput },
  props: {
    image: { type: Object, required: true }
  },
  data() {
    const col = (name, x = {}) => ({
      name,
      align: "left",
      field: name,
      label: name,
      sortable: true,
      ...x
    });
    const columns = [col("operation"), col("argument", { autoWidth: false })];
    return { columns };
  }
};
</script>
