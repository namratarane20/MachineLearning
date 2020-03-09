<template>
    <div>
        <h2 style="text-align:center">Example of firing an event form child component to parent</h2>
        
        <h3> {{ message }} </h3>

        <button @click="changeConetnt">change content</button>
    </div>
</template>

<script>
export default {
    props : {
        message : String
    },
    methods : {
        changeConetnt() {
            // this.message = "changed from child component"
            this.$emit("updateMsg","changed from child component")
        }
    }
}
</script>