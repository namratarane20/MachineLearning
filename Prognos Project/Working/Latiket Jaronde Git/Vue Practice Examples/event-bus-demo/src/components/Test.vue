<template>
  <div id="app">
      <h3> {{ msg }} </h3>
  </div>
</template>

<script>

import {EventBus} from '../main.js'

export default {
  name: 'app',
  data () {
    return {
        msg : "default msg inside est component"
    }
  },
  mounted() {
      EventBus.$on("emittedData", data => {
          this.msg = data
      })
  }
}
</script>

<style>
</style>
