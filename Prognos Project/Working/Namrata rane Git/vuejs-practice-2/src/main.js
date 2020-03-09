import Vue from 'vue'
import App from './App.vue'
import Content from './components/Content.vue'
Vue.component("Content",Content)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
