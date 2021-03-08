<template>
  <div class=" row q-col-gutter-md q-py-md">
    <div class="col col-6">
      <q-card>
        <q-card-section>
          <div class="row items-center q-gutter-md">
            <div class="text-h6">Informations</div>
            <q-space />
            <HelpLink
              href="https://doc.powerdns.com/authoritative/http-api/zone.html"
            />
          </div>
        </q-card-section>
        <q-card-section class="q-col-gutter-md">
          <div>
            <q-list dark separator>
              <q-item>
                <q-item-section>
                  <q-item-label overline>Zone</q-item-label>
                  <q-item-label>{{ rule.zone }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label overline>Name</q-item-label>
                  <q-item-label>{{ rule.name }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label overline>Type</q-item-label>
                  <q-item-label>{{ rule.type }}</q-item-label>
                </q-item-section>
              </q-item>
              <q-item>
                <q-item-section>
                  <q-item-label overline>TTL</q-item-label>
                  <q-item-label>
                    <div>
                      <q-input type="number" dense v-model="ttl">
                        <template v-slot:after>
                          <ResetAndSave
                            size="sm"
                            padding="sm"
                            :modified="ttl != rule.ttl"
                            @save="updateTTL"
                            @reset="ttl = rule.ttl"
                          />
                        </template>
                      </q-input>
                    </div>
                  </q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <div class="col col-6">
      <EditTable
        title="Records"
        :columns="recordColumns"
        :createDefault="createRecord"
        v-model="records"
        @submit="updateRecords"
      >
        <template v-slot:body-cell-enabled="props">
          <q-td>
            <div class="row">
              <q-space />
              <q-toggle slot="" v-model="props.row['enabled']" />
            </div>
          </q-td>
        </template>
      </EditTable>
    </div>
    <div class="col col-12">
      <LogList :domain="rule.name" :type="rule.type"/>
    </div>
  </div>
</template>
<script>
import EditTable from "src/components/EditTable.vue";
import HelpLink from "src/components/HelpLink.vue";
import LogList from "src/components/DNS/LogList.vue";

import graphql from "src/gql/dns";
const {
  mutations: { updateTLLForDnsRule, updateRecordsForDnsRule }
} = graphql;

import ResetAndSave from "src/components/ResetAndSave.vue";
export default {
  components: { EditTable, ResetAndSave, HelpLink, LogList },
  props: {
    rule: Object
  },
  data() {
    const recordColumns = [
      {
        name: "content",
        align: "left",
        label: "content",
        field: "content",
        headerStyle: "width: 90%"
      },
      {
        name: "enabled",
        align: "left",
        label: "enabled",
        field: "enabled",
        headerStyle: "width: 10%"
      }
    ];
    return { ttl: 0, recordColumns, records: [] };
  },
  methods: {
    updateRecords() {
      const variables = {
        zone: this.rule.zone,
        name: this.rule.name,
        type: this.rule.type,
        records: this.records
      };
      this.runMutation(
        updateRecordsForDnsRule,
        variables,
        `Records updated for ${this.rule.type} ${this.rule.name}`
      );
    },
    createRecord() {
      return { content: "", enabled: true };
    },
    updateTTL() {
      const variables = {
        zone: this.rule.zone,
        name: this.rule.name,
        type: this.rule.type,
        ttl: this.ttl
      };
      this.runMutation(
        updateTLLForDnsRule,
        variables,
        `TTL updated for ${this.rule.type} ${this.rule.name}`
      );
    }
  },
  computed: {
    ruleTTL() {
      return this.rule.ttl;
    },
    ruleRecords() {
      return this.rule.records;
    }
  },
  watch: {
    ruleRecords: {
      immediate: true,
      handler(records) {
        this.records = records.map(({ content, enabled }) => ({
          content,
          enabled
        }));
      }
    },
    ruleTTL: {
      handler(ttl) {
        this.ttl = ttl;
      },
      immediate: true
    }
  }
};
</script>

<style></style>
