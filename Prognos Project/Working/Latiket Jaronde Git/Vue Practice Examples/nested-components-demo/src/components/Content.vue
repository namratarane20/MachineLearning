<template>
  <div class = "contentClass">
      <h1>{{ msg }}</h1>
          <li v-for="list in myplaylist" :key="list" style="font-size : 15px">
              <a :href="list.link1" target="_blank"> {{ list.name1 }} </a>
          </li>
    
    <hr>
    <li v-for="st in studentlist" :key="st">
        {{ st }}
    </li>
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
        msg : "unbox therapy content list"
    }
  },
  props : {
      myplaylist : Array,
      studentlist : Array
  }
}
</script>

<style>
.contentClass {
    color : black;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    margin-top: 5px;
    text-align: center;
    margin-bottom: 3px
}
</style>
