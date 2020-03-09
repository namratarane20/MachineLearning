<template>
  <div >

      <button @click="passData">click here</button>

  </div>
</template>

<script>

import {EventBus} from '../main.js'

export default {
  data () {
    return {

    }
  },
  methods : {
      passData() {
          console.log("clicked on button")

          EventBus.$emit("emittedData","data passed from student component")
      }
  }
}
</script>

<style>
</style>
