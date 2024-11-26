<template>
  <div>
    <LibraryContentsVideo />
  </div>
</template>

<script>
import LibraryContentsVideo from "@/components/Library/LibraryContentsVideo.vue";

export default {
  name: "LibraryContentsPageView",
  components: {
    LibraryContentsVideo,
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
