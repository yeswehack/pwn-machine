/<template>
  <div class="row justify-center">
    <div class="column col q-gutter-md" style="max-width:800px">
      <div class="text-h6">Create a new shell</div>
      <ContainerSelect
        allowNew
        v-model="config.container"
        :filter="onlyRunningContainer"
        @input="updateImage"
      />
      <ImageSelect v-model="config.image" v-if="newContainer" />
      <VolumeSelect v-model="config.volumes" v-if="newContainer" />
      <NetworkSelect v-model="config.networks" v-if="newContainer" />
      <KeyValueTable
        title="Environment"
        class="bg-grey-9"
        v-model="config.env"
      />
      <q-input v-model="config.cmd" filled dense label="command" />

      <div class="row q-gutter-md">
        <q-toggle label="Privileged" v-model="config.privileged" />
        <q-space />
        <q-btn label="Run" color="positive" />
      </div>
      <div class="q-mt-lg">
        {{ config }}
      </div>
    </div>
  </div>
</template>

<script>
import ImageSelect from "src/components/Docker/Container/Form/ImageSelect.vue";
import ContainerSelect from "src/components/Docker/Container/Form/ContainerSelect.vue";
import VolumeSelect from "src/components/Docker/Container/Form/VolumeSelect.vue";
import NetworkSelect from "src/components/Docker/Container/Form/NetworkSelect.vue";
import KeyValueTable from "src/components/KeyValueTable.vue";
import { fetchAll } from "src/store/docker/actions";
export default {
  components: {
    ImageSelect,
    ContainerSelect,
    VolumeSelect,
    NetworkSelect,
    KeyValueTable
  },
  created() {
    this.fetchAll();
  },
  data() {
    return {
      config: {
        container: null,
        image: null,
        volumes: [],
        networks: [],
        privileged: false,
        env: {},
        cmd: "/bin/sh -c 'if which bash; then bash ; else sh ; fi' "
      }
    };
  },
  methods: {
    updateImage(container) {
      if (container === null || container === "New container") {
        this.config.image = "";
      } else {
        const c = this.containers.find(c => c.Name == container);
        const image = c.Config.Image;
        this.config.image = image.includes(":") ? image : `${image}:latest`;
      }
    },
    fetchAll() {
      this.$store.dispatch("docker/fetchAll");
    },
    onlyRunningContainer(c) {
      return c.State.Running;
    }
  },
  computed: {
    newContainer() {
      return this.config.container == "New container";
    },
    containers() {
      return this.$store.getters["docker/containers"];
    },
    images() {
      return this.$store.getters["docker/images"];
    },
    volumes() {
      return this.$store.getters["docker/volumes"];
    }
  }
};
</script>

<style></style>
