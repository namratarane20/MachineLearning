<template>
    <div>
        <slot name="header"></slot>
        <h1> {{ msg }} </h1>
        <slot></slot>
        <slot name="para"></slot>
    </div>
</template>

<script>
export default {
    data() {
        return {
            msg : "slots in VueJS demo"
        }
    }
}
</script>

<style scoped>
h1 {
    text-align: center;
    background-color: blue;
}
</style>