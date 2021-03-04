<template>
  <q-table
    title="Networks"
    hide-pagination
    hide-no-data
    dense
    :pagination="pagination"
    :data="data"
    :columns="columns"
    row-key="name"
  >
    <template #body-cell-name="props">
      <q-td>
        <div>
          <NetworkLink :name="props.value" />
        </div>
      </q-td>
    </template>
    <template #bottom>
      <div class="col-12 row justify-end q-gutter-md">
        <div class="col-auto">Exposed ports:</div>
        <div class="col-auto bg-">
          <PortList :settings="settings" />
        </div>
      </div>
    </template>
  </q-table>
</template>

<script>
import PortList from "src/components/Docker/Container/PortList.vue";
import NetworkLink from "src/components/Docker/Network/Link.vue";
export default {
  components: { PortList, NetworkLink },
  props: {
    settings: Object
  },
  data() {
    const networks = this.settings.Networks;
    const ports = this.settings.Ports;
    const columns = [
      {
        name: "name",
        label: "Name",
        align: "left",
        field: "Name"
      },
      {
        name: "hostname",
        label: "Hostname",
        align: "left",
        field: "Aliases",
        format: v => (v ? v.join(", ") : "n/a")
      },
      {
        name: "ip",
        label: "IP",
        align: "left",
        field: "IPAddress"
      },
      {
        name: "mac",
        label: "MAC",
        align: "left",
        field: "MacAddress"
      }
    ];

    const pagination = {
      rowsPerPage: 0
    };
    const data = Object.entries(networks).map(([name, network]) =>
      Object.assign(network, { Name: name })
    );
    return { pagination, data, columns };
  }
};
</script>

<style></style>
