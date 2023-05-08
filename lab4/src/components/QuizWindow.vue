<template>
  <div class="bg-cover bg-center ... min-h-screen" style="background-color:#446879;">
    <div class="pt-10">
      <div v-if="quizzes.length">
        <div class="max-w-2xl mx-auto py-16 px-4 sm:py-10 sm:px-6 lg:max-w-7xl lg:px-8">
          <div class="mt-6 grid grid-cols-1 gap-y-20 gap-x-10 sm:grid-cols-2 lg:grid-cols-4 xl:gap-x-8">
            <div v-for="quiz in quizzes" :key="quiz.id" class="group relative">
              <router-link :to="{name: 'quiz', params: {id: quiz.id}}">
                <div class=" top-50 min-h-100 aspect-w-2 aspect-h-2 rounded-md overflow-hidden group-hover:opacity-75 lg:h-100 lg:aspect-none">
                  <img src="../assets/sushi.jpg" class="w-full h-full object-center object-cover lg:w-full lg:h-full" />
                </div>
                <div class="mt-4 flex justify-between">
                  <div>
                    <h3 class="text-sm text-white font-bold">
                      <a href="#">
                        <span aria-hidden="true" class="absolute inset-0" />
                        {{ quiz.title }}
                      </a>
                    </h3>
                  </div>
                  <p class="text-sm font-medium text-white">{{ quiz.questions_count }}</p>
                </div>
              </router-link>
            </div>
          </div>
        </div>
        <router-view></router-view>
      </div>
      <div v-else>
        <p>Loading quizzes...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      quizzes:[]
    }
  },
  mounted() {
    fetch('https://late-glitter-4431.fly.dev/api/v54/quizzes', {
      headers: {'X-Access-Token': '50f1a5fded92970d2c46d4649605aedd0ed8d319f2f27da183eecf6b8b9af6cc'}
    })
        .then(response => response.json())
        .then(data => this.quizzes = data)
        .then(data => console.log(data))
        .catch(error => console.log(error.message))
  },
}
</script>

<style scoped>

</style>
