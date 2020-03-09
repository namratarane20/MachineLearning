<template>
  <div id="app">
    <fib ></fib>

    <br><hr><br>

    <cbb></cbb>
  </div>
</template>

<script>

import FormInputBinding from './components/FromInputBinding.vue'
import CheckboxBinding from './components/CheckBoxBinding.vue'

export default {
  components: {
    "fib" : FormInputBinding,
    "cbb" : CheckboxBinding
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
