import Vue from 'vue'
import App from './App.vue'
import Student from './Student.vue'

Vue.component("std",Student)

new Vue({
  el: '#app',
  render: h => h(App)
})
