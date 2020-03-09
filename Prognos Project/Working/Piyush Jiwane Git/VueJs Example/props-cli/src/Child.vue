<template>
  <div>
      Hi....
      <br>
      {{ name }}
      <br><br>
      <ul v-for="list in myPlayList">
          <li>{{ list }}</li>
      </ul>
      <br><br>
      {{ channelName }}
  </div>
</template>

<script>
export default {
 props:["name","myPlayList","channelName"],
  data () {
    return {
     
    }
  }
}
</script>

<style>

</style>
