<template>
    <div id="sapp">
        <h3>{{ msg }}</h3>
        <ol>
            <li v-for="st in students" :key="st">
                {{ st }}
            </li>
        </ol>

    </div>
</template>

<script>
export default {
    name : "student",
    data () {
        return {
            msg : "inside student component",
            students : ["a","b","c","d"]
        }
    }
}
</script>

<style scoped>
  h3 {
    color : blue;
    font-size: 30px
  }
</style>