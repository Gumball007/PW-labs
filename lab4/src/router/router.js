import { createWebHistory, createRouter } from "vue-router";
import Register from "../components/Register.vue";
import QuizWindow from "../components/QuizWindow.vue";
import Home from "../components/Home.vue";
import QuizElement from "../components/QuizElement.vue";
import HeroPage from "../components/HeroPage.vue";
import HeroQuizzes from "../components/HeroQuizzes.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        children: [
            {
                path: "",
                name: "HeroPage",
                component: HeroPage,
            },
            {
                path: "/quizzes",
                name: "QuizWindow",
                component: HeroQuizzes,
                children: [
                    {
                        path: ":id",
                        name: "quiz" ,
                        component: QuizElement,
                    },
                    {
                        path: "",
                        name: "all_quizzes" ,
                        component: QuizWindow,
                    },
                ]
            },
            {
                path: "/register",
                name: "Register",
                component: Register,
            },

        ]
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
