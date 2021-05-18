<template>
  <q-page padding class="page">
    <q-tabs
      dense
      rounded
      inline-label
      shadow
      class="text-white bg-dark rounded-borders tabs q-pr-sm"
      active-color="primary"
      align="left"
      narrow-indicator
      v-mutation="hookNavigation"
    >
      <slot name="default"></slot>
    </q-tabs>
    <div
      class="row justify-center bg-dark q-pa-md page-content rounded-borders"
    >
      <transition @before-enter="beforeEnter" @before-leave="beforeLeave">
        <router-view class="animated" :key="$route.path" />
      </transition>
    </div>
  </q-page>
</template>

<script>
export default {
  data() {
    return {
      oldIdx: null,
      oldSlots: null
    };
  },
  mounted() {
    this.hookNavigation();
  },
  methods: {
    hookNavigation() {
      if (this.oldSlots == this.$slots) return;
      for (const [idx, { elm }] of this.$slots.default.entries()) {
        if (elm.getAttribute("aria-current") == "page") {
          this.oldIdx = idx;
        }
        elm.setAttribute("aria-idx", idx);
      }
      this.oldSlots = this.$slots;
    },
    beforeEnter(el){
      const linkEl = document.activeElement.parentElement;
      const newIdx = linkEl.getAttribute("aria-idx");
      const slideOut = newIdx < this.oldIdx ? "slideInLeft" : "slideInRight";
      el.classList.add(slideOut);
    },
    beforeLeave(el) {
      const linkEl = document.activeElement.parentElement;
      const newIdx = linkEl.getAttribute("aria-idx");
      const slideOut = newIdx < this.oldIdx ? "slideOutRight" : "slideOutLeft";
      this.oldIdx = newIdx;
      el.classList.add(slideOut);

      const { width, height } = el.getBoundingClientRect();
      Object.assign(el.style, {
        width: `${width}px`,
        height: `${height}px`,
        position: "absolute",
        top: "76px",
        left: "16px"
      });
    }
  }
};
</script>
<style lang="scss" scoped>
.page-content {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
  overflow-x: hidden;

  // Hacky way to hide children transition overflow
  &::before,
  &::after {
    content: "";
    width: 24px;
    position: absolute;
    top: 0;
    height: 100%;

    background: #121212;
    z-index: 100;
  }
  &::before {
    left: 0px;
  }
  &::after {
    right: 0px;
  }
}
.page .tabs {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  text-decoration: none;
}
.page {
  display: grid;
  width: 100%;
  grid-template-columns: 100%;
  grid-template-rows: auto 1fr;
  flex-direction: column;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14),
    0 3px 1px -2px rgba(0, 0, 0, 0.12);
  overflow-x: hidden;
}
</style>
<style>
.tabs a {
  text-decoration: none;
}
</style>
