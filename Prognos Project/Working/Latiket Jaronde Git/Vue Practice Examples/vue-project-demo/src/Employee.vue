<template>
    <div id="eapp">
        <h3>{{ msg }}</h3>

        <ol>
            <li v-for="e in employees" :key="e"> 
                {{ e }}
            </li>
        </ol>
    </div>
</template>

<script>
export default {
    name : "employee",
    data () {
        return{
            msg : "inside employee component",
            employees : ["emp1","emp2","emp3"]
        }
    }
}
</script>