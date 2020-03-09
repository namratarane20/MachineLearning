<template>
  <div class="footerClass">
    {{ msg }}
  </div>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      msg : "this is footer"
    }
  }
}
</script>

<style>

.footerClass {
    background-color: red;
    color : black;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 20px;
    text-align: right;
    margin-top: 5px
}
</style>
