<template>
<div>
<ul>
        <li v-for="student in students">
{{ student }}
        </li>
    </ul>
</div>
    
</template>
<script>
export default {
    data(){
return{
    students:["abc","bcd","cde","def"]
}
    }
}
</script>
<style scoped>

</style>