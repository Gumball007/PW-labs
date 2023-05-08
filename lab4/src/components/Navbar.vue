<template>
  <nav class="top-0 absolute z-50 w-full flex items-center justify-between px-2 py-3">
    <div class="container px-4 mx-auto flex items-center justify-between lg:mx-auto">
      <div class="w-full flex justify-between lg:w-auto lg:static lg:block lg:justify-start">
        <button
          class="text-white cursor-pointer text-xl leading-none px-3 py-1 border border-solid border-transparent rounded bg-transparent block lg:hidden outline-none focus:outline-none"
          type="button"
          v-on:click="toggleNavbar()">
          <img class="h-8 w-auto" src="../assets/menu.svg" />
        </button>
      </div>

      <div class="hidden lg:flex items-center justify-center w-full">
        <div class="flex justify-center">
          <router-link :to="{name: 'HeroPage'}">
            <div class="text-sm font-bold leading-relaxed inline-block mr-4 py-2 whitespace-nowrap uppercase text-white">
              <img class="h-20 w-auto" src="../assets/quizit_logotype.svg" />
            </div>
          </router-link>
        </div>
      </div>

      <div class="lg:flex flex-grow items-center lg:bg-transparent lg:shadow-none">
        <ul class="flex flex-col lg:flex-row list-none mr-auto">
          <li class="mr-auto">
            <div class="flex items-center py-3 px-4 hover:bg-[#253f4b] rounded hover:text-white-200 transition duration-200">
              <router-link :to="{name: 'all_quizzes'}">
                <span class="text-white px-1 font-bold" @click="getQuizzes">Quizzes</span>
              </router-link>
            </div>
          </li>
        </ul>
        <div class="flex items-center py-3 px-4 hover:bg-[#253f4b] rounded hover:text-blue-200 transition duration-200 ml-auto">
          <router-link :to="{name: 'Register'}">
            <span class="text-white px-1 font-bold">Register</span>
          </router-link>
        </div>
      </div>
    </div>
</nav>  
</template>

<script>
export default {
  data() {
    return {
      showMenu: false
    };
  },
  methods: {
    toggleNavbar: function() {
      this.showMenu = !this.showMenu;
    },
    async getQuizzes() {}
  }
};
</script>
