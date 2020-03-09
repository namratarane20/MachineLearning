<template>
    <div>
        <h1>
            Data Binding concepts
        </h1>
        <p v-bind="link"> press here</p>
        <a v-bind:href="link" v-bind:title="title"> {{ name }}
        <img v-bind:src="imgLink"></a>
    </div>
</template>
<script>
export default {
    data(){
        return{
            link:"https://www.google.com",
            name:"this is our link",
            title:" connect to  google.com site",
            imgLink:"@/assets/rose.jpeg"
        }
    }
}
</script>
