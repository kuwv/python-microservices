import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home.vue';
import Protected from './components/Protected.vue';
import Profile from './components/Profile.vue';
import About from './components/About.vue';


Vue.use(Router);

const router = new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/protected',
      name: 'protected',
      component: Protected,
      meta: {
        isSecure: true,
      }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: {
        isSecure: true,
      }
    },
    {
      path: '/about',
      name: 'about',
      component: About
    },
    // { 
    //   path: '*',
    //   name: '404',
    //   component: NotFoundComponent
    // }
  ]
});

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.isSecure)) {
    // this route requires auth, check if logged in
    // if not, redirect to login page.
    Vue.prototype.$auth.isUserAuthenticated().then((isAuthenticated) => {
      if (isAuthenticated) {
        next()
      }
      else {
        next({
          path: '/',
          query: { redirect: to.fullPath }
        })
      }
    });
  } else {
    next();
  }
});

export default router;