import Vue from 'vue'
import './plugins/fontawesome'
import App from './App.vue'
import 'jquery';
import 'bootstrap';
import 'popper.js';
import './assets/app.scss'

// import { faCoffee } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// library.add(faCoffee)

Vue.component('font-awesome-icon', FontAwesomeIcon)






import Header from './components/Header.vue'
import Footer from './components/Footer.vue'
Vue.component("Header",Header)
Vue.component("Footer",Footer)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
