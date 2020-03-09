<template>
  <div >
      <h3>{{ msg }}</h3>
  </div>
</template>

<script>

import {EventBus} from '../main.js'

export default {
  name: 'app',
  data () {
    return {
        msg : "msg in employee component"
    }
  },
  methods : {
      
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
