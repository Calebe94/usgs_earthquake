import Vue from "vue";
import Router from "vue-router";
import Home from "@/components/Home.vue";
import Results from "@/components/Results.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "Home",
      component: Home,
      meta: {
        title: "USGS Earthquake - Code Challenge",
      },
    },
    {
      path: "/results",
      name: "Results",
      component: Results,
    },
  ],
});
