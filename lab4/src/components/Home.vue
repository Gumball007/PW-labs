<template>
  <div class="bg-[#253f4b]">
    <Navbar></Navbar>
  </div>
  <router-view />
</template>

<script>
import Navbar from "./Navbar.vue"
import QuizWindow from "./QuizWindow.vue";
import Register from "./Register.vue";

export default {
  name: "Home",
  components: {QuizWindow, Navbar}
}
</script>

<style scoped>

</style>
