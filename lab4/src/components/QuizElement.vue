<template>
  <div class="bg-cover bg-center ... min-h-screen" style="background-color:#446879">
    <div class="pt-36">
      <main class="flex h-11/12 items-center justify-center bg-white-100">

        <QuizComplete v-if="endQuiz"
                      :percent="percentageScore"/>
        <!-- quiz container -->
        <div
            class="overflow-hidden bg-white flex-none container relative shadow-lg rounded-lg px-12 py-4"
        >
          <!-- contents -->
          <div class="relative z-15">
            <!-- score container -->
            <div class="text-right text-gray-800">
              <p class="text-sm leading-3">Score</p>
              <p class="font-bold">{{ score }} points</p>
            </div>

            <!-- timer container -->
            <div class="bg-white shadow-lg p-1 rounded-full w-full h-5 mt-4">
              <div class="bg-[#365563] rounded-full w-11/12 h-full"
                   :style = "`width:${timer}%`">
              </div>
            </div>

            <!-- question container -->
            <div
                class="rounded-lg bg-gray-100 p-2 neumorph-1 text-center font-bold text-gray-800 mt-8"
            >
              <div class="bg-white p-3 rounded-lg">
                {{ currentQuestion.question }}
              </div>
            </div>

            <!-- options container -->

            <div class="mt-6">
              <!-- option container -->
              <div v-for="(choice, item) in currentQuestion.answers" :key="item">
                <div
                    class="neumorph-1 option-default bg-gray-100 p-2 rounded-lg mb-3 relative"
                    :ref="optionChosen"
                    @click="onOptionClick(choice, item)">
                  <div
                      class="bg-[#365563] p-1 transform rotate-45 rounded-md h-10 w-10 text-white font-bold absolute right-0 top-0 shadow-md"
                  >
                    <p class="transform -rotate-45">+10</p>
                  </div>
                  <div class="rounded-lg font-bold flex p-2">
                    <!-- option ID -->
                    <div class="p-3 rounded-lg">{{ item }}</div>

                    <!-- option name -->
                    <div class="flex items-center pl-6">{{ choice }}</div>
                  </div>
                </div>
              </div>

              <!-- progress indicator container -->
              <div class="mt-8 text-center">
                <div class="h-1 w-12 bg-[#365563] rounded-full mx-auto"></div>
                <p class="font-bold text-gray-800">{{ questionCounter }}</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.neumorph-1 {
  box-shadow: 6px 6px 18px rgba(0, 0, 0, 0.09), -6px -6px 18px #ffffff;
}
.container {
  max-width: 400px;
  border-radius: 25px;
}
</style>

<script>
import {onMounted, ref} from "vue";
import QuizComplete from "./QuizComplete.vue";
import {useStore} from "vuex";
import {useRoute} from "vue-router";

export default {
  setup() {
    let canCLick = true
    let timer = ref(100)
    let endQuiz = ref(false)
    let questionCounter = ref(0)
    let score = ref(0)
    let percentageScore = ref(0)
    const store = useStore()
    const route = useRoute()
    const currentQuestion = ref({
      question: "",
      answers: [],
      correct_answer: ""
    });

    let questions = ref([])

    const loadQuestion = () => {
      canCLick = true
      if(questions.length > questionCounter.value) {
        // load question
        timer.value = 100
        currentQuestion.value = questions[questionCounter.value]
        questionCounter.value++
      } else {
        // no more questions
        onQuizEnd()
        console.log("Out of questions")
      }
    }

    let itemsRef = []
    const optionChosen = (element) => {
      if(element) {
        itemsRef.push(element)
      }
    }

    const countDownTimer = function() {
      let interVal = setInterval(() => {
        if (timer.value > 0) {
          timer.value--
        } else {
          console.log("timer is up")
          onQuizEnd()
          clearInterval(interVal)
        }
      }, 150)
    }

    const clearSelectedAnswer = (divSelected) => {
      setTimeout(() => {
        divSelected.classList.remove("option-correct")
        divSelected.classList.remove("option-wrong")
        divSelected.classList.add("option-default")
        loadQuestion()
      }, 1000)
    }

    const onOptionClick = (choice, item) => {
      if(canCLick) {
        const divContainer = itemsRef[item]
        fetch(`https://late-glitter-4431.fly.dev/api/v54/quizzes/${route.params.id}/submit`, {
          headers: {
            'X-Access-Token': '50f1a5fded92970d2c46d4649605aedd0ed8d319f2f27da183eecf6b8b9af6cc',
            'Content-Type': 'application/json',
          },
          method: "POST",
          body: JSON.stringify({
            "data": {
              "question_id": currentQuestion.value.id,
              "answer": choice,
              "user_id": store.state.user.id
            }
          })
        })
          .then(response => response.json())

          .then((data) => {
            console.log(data.correct)
            if (data.correct === true) {
              console.log('You are correct')
              score.value += 10
              divContainer.classList.add("option-correct")
              divContainer.classList.remove("option-default")

          } else {
            console.log('You are wrong')
            divContainer.classList.add("option-wrong")
            divContainer.classList.remove("option-default")
          }
          timer.value = 100
          canCLick = false
          clearSelectedAnswer(divContainer)
          console.log(choice, item)
        })
      } else {
        console.log("Can not select an option")
      }
    }

    const fetchQuestions = async function () {
      console.log("Fetch questions")
      fetch(`https://late-glitter-4431.fly.dev/api/v54/quizzes/${route.params.id}?user_id=${store.state.user?.id}`, {
        headers: {'X-Access-Token': '50f1a5fded92970d2c46d4649605aedd0ed8d319f2f27da183eecf6b8b9af6cc'}
      })
        .then((response) => {
          return response.json()
        })
        .then((data) => {
          console.log(data)
          const newQuestions = data.questions.map((serverQuestion) => {
            const  arrangedQuestion = {
              id: serverQuestion.id,
              question: serverQuestion.question,
              answers: serverQuestion.answers,
            }
            return arrangedQuestion
          })
          console.log("new formatted questions", newQuestions)
          questions = newQuestions
          loadQuestion()
          countDownTimer()
      })
    }

    const onQuizEnd = function () {
      percentageScore.value = parseFloat((score.value * 100) / (questions.length * 10)).toFixed(1)
      timer.value = 0
      endQuiz.value = true
    }

    onMounted(() => {
      fetchQuestions()
    })
    return { currentQuestion, questions, questionCounter, score, timer, endQuiz, percentageScore, loadQuestion, onOptionClick, optionChosen };
  },
  components: {
    QuizComplete
  }
}
</script>
