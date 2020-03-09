import Vue from 'vue'
import App from './App.vue'
import GlobalComponent from './components/GlobalComponent.vue'
Vue.component("GlobalComponent",GlobalComponent)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
