<template>
  <div id="app">
    <slt>
      <h3 slot="header"> This is h3 heading in App.vue component </h3>
      <p slot="para"> This is paragraph in App component </p>
      <p>this is just a slot</p>
    </slt>
  </div>
</template>

<script>

import Slots from './components/Slots.vue'

export default {
  components: {
    "slt" : Slots
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
