<template>
  <q-card>
    <q-card-section>
      <div class="text-h6">Processes</div>
    </q-card-section>
    <q-card-section>
      <q-table
        flat
        :data="processes"
        table-header-style="text-transform: capitalize"
        :columns="columns"
        hide-bottom
        :rows-per-page-options="[0]"
      >
        <template #body-cell="props">
          <q-td :props="props" auto-width>{{ props.value }}</q-td>
        </template>
        <template #body-cell-command="props">
          <q-td
            :props="props"
            class="text-align-left ellipsis"
            style="max-width: 40vw;"
            align="left"
          >
  
  
            {{ props.value }}
            <q-popup-edit :value="props.value">
              <q-input :value="props.value" readonly dense autofocus counter />
            </q-popup-edit>
          </q-td>
        </template>
      </q-table>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  props: {
    processes: { type: Array, required: true }
  },
  data() {
    const col = (name, props = {}) => ({
      name,
      label: name,
      sortable: true,
      field: name,
      ...props
    });
    const columns = [
      col("user"),
      col("pid"),
      col("cpu"),
      col("mem"),
      col("tty"),
      col("stat"),
      col("start"),
      col("time"),
      col("command", { align: "left" })
    ];
    return { columns };
  }
};
</script>
