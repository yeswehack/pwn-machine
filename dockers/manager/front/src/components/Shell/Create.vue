<template>
  <div>
    <q-card-section>
      <div class="column q-gutter-md">
        <component
          :is="formChildren.containerName"
          v-model="form.containerName"
        />
        <q-input label="Command" v-model="form.cmd" />

        <q-list separator class="rounded-borders" bordered>
          <q-expansion-item label="Extra config" icon="star">
            <q-card>
              <q-card-section>
                <div class="column q-col-gutter-sm">
                  <div class="col">
                    <q-input
                      label="User"
                      v-model="form.user"
                      hint="format: <name|uid>[:<group|gid>]"
                    />
                  </div>
                  <div class="col">
                    <q-input label="Working directory" v-model="form.workdir" />
                  </div>
                  <div class="col">
                    <q-toggle label="Privileged" v-model="form.privileged" />
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </q-expansion-item>
          <component
            :is="formChildren.environment"
            v-model="form.environment"
          />
        </q-list>
      </div>
    </q-card-section>
    <q-card-section>
      <reset-and-save :modified="modified" @save="submit" @reset="reset" />
    </q-card-section>
  </div>
</template>

<script>
import DeepForm from "src/mixins/DeepForm";
import ContainerSelect from "../Docker/Container/Form/ContainerSelect.vue";
import EnvironInputVue from "../Docker/Container/Form/EnvironInput.vue";
import ResetAndSave from "../ResetAndSave.vue";
import api from "src/api";
export default {
  mixins: [DeepForm],
  formDefinition: {
    user: null,
    workdir: null,
    privileged: false,
    cmd: "/bin/sh -c 'if which bash; then bash ; else sh ; fi'",
    containerName: ContainerSelect,
    environment: EnvironInputVue
  },
  components: { ContainerSelect, ResetAndSave },
  methods: {
    submit() {
      this.$apollo
        .mutate({
          mutation: api.docker.SPAWN_CONTAINER_SHELL,
          variables: { input: this.form },
          refetchQueries: [{ query: api.docker.GET_CONTAINER_SHELLS }]
        })
        .then(({ data }) => {
          const uuid = data.dockerSpawnContainerShell.nodeId;
          this.$router.push({ name: "shellId", params: { uuid } });
        });
    }
  }
};
</script>

<style>
.no-top-border {
  border-top: none;
}
</style>
