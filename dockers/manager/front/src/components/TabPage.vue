<template>
  <q-page padding class="page" ref="page">
    <q-tabs
      dense
      rounded
      inline-label
      shadow
      ref="tabs"
      class="text-white bg-dark rounded-borders tabs q-pr-sm"
      indicator-color="primary"
      align="left"
    >
      <slot name="default"></slot>
    </q-tabs>
    <div
      class="row justify-center bg-dark q-pa-md page-content rounded-borders"
    >
      <div class="col relative">
        <transition name="slide">
          <router-view ref="view" :key="$route.path" class="view"></router-view>
        </transition>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  watch: {
    $route(to, from) {
      const links = Array.from(this.$refs.tabs.$el.querySelectorAll(".q-tab"));
      const findPos = route =>
        links.findIndex(l => l.attributes.href.value == route.path);

      const oldIdx = findPos(from);
      const newIdx = findPos(to);
      const direction = newIdx < oldIdx ? 1 : -1;
      this.$refs.page.$el.style.setProperty("--direction", direction);
    }
  }
};
</script>
<style lang="scss" scoped>
.page-content {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  overflow-x: hidden;
}
.page .tabs {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  text-decoration: none;
}
.view {
  top: 0;
  height: 100%;
}
.relative {
  position: relative;
  overflow: hidden;
}
.page {
  --direction: 1;
  display: grid;
  width: 100%;
  grid-template-columns: 100%;
  grid-template-rows: auto 1fr;
  flex-direction: column;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14),
    0 3px 1px -2px rgba(0, 0, 0, 0.12);
  overflow-x: hidden;
}
.slide-enter-active,
.slide-leave-active {
  position: absolute;
  transition: 300ms;
}

.slide-enter {
  transform: translateX(calc(100% * -1 * var(--direction)));
}
.slide-enter-to {
  transform: translateX(0);
}

.slide-leave {
  transform: translateX(0);
}
.slide-leave-to {
  transform: translateX(calc(100% * var(--direction)));
}
</style>
<style>
.tabs a {
  text-decoration: none;
}
</style>
