<template>
  <div>
    <div>
      {{ msg }}
      <ul v-for="nameList in studentsList">
        <li>{{ nameList }}</li>
      </ul>
    </div>
    <div>{{ wish("Evening")}} -- {{ fullName }}</div>
    <br>
    <div>
      <std></std><br>
      <employee></employee>
    </div>
  </div>
</template>

<script>

import Employee from "./Employee.vue"
export default {
  components:{
    "employee":Employee
  },
  data() {
    return {
      studentsList: ["Piyush", "Gaurav", "Anil", "Vanmala"],
      msg: "Welcome to Your Vue.js App",
      firstName: "Piyush ",
      lastName: "Jiwnae"
    };
  },
  methods: {
    wish(dayTime) {
      return "Good " + dayTime;
    }
  },
  computed: {
    fullName() {
      return this.firstName + this.lastName;
    }
  }
};
</script>

<style>
</style>
