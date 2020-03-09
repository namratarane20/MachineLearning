<template>
  <div class="headerClass">
    {{ msg }}
    <br />
    <h6>Author name : {{ authorname }} </h6>
  </div>
</template>

<script>
export default {
  data() {
    return {
      msg: "This contennts playlist"
    }
  },
  props: {
    authorname: String
  }
};
</script>

<style scoped>
.headerClass {
  background-color: blue;
  color: black;
  font-family: Arial, Helvetica, sans-serif;
  font-size: 30px;
  text-align: center;
  margin-bottom: 3px;
}
</style>
