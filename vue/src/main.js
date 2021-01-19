// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'es6-shim'

import Vue from 'vue'
import N3 from 'N3-components'
import 'N3-components/dist/index.min.css'
import axios from './utils/axios'
import extend from './extend'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(axios)
Vue.use(extend)
Vue.use(N3)
Vue.use(ElementUI)

import App from './App'
import router from './router'
import store from './store'
import './assets/styles/base.css'

/* eslint-disable */
new Vue({
  el: '#app',
  template: '<App />',
  components: { App },
  router,
  store
})
/* eslint-enable */
