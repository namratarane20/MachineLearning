import Vue from 'vue'
import App from './App.vue'
import 'jquery';
import 'bootstrap';
import './assets/app.scss';
import 'popper.js';


// import 'maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css'


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
