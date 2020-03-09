<template>
  <div>
    <h3>{{ msg }}</h3>    
     <hr>
    <h3>{{ msg2 }}</h3>

    <br><hr><br>
     <p>
       <ul>
         <li v-for="s in students"  v-bind:key="s"> {{ s }} </li>
       </ul>
     </p>

     <br><hr><br>
     {{ wish("morning") }}

     <br><hr><br>
     {{ comp }}

     <br><hr><br>
     <student></student>
     <br><hr><br>
     <employee></employee>

  </div>
</template>

<script>

import Employee from './Employee.vue' //importing component

export default {
  components: {
    "employee" : Employee //locally registering Employee.vue and it'll be accessible in only App.vue
  },
  data () {
    return {
      students : ["akash", "sidhanth", "sudha", "abhi", "hemya"],
      msg: 'Welcome to Your Vue.js App',
      msg2 : "second mmsg",
      fname : "kobe",
      lname : "bryant"
    }
  },
  methods : {
    wish(somethhing) {
      return "Good " + somethhing
    }
  },
  computed : {
    comp() {
      return this.fname + " " + this.lname
    }
  }
}
</script>

<style scoped>
  h3 {
    color : red;
    font-size: 30px
  }
</style>
