<template>
    <div>
        <h2> {{ msg }} </h2>
        <ol>
            <li v-for="st in studentlist" :key="st">
                {{ st }}
            </li>
        </ol>

        <button @click="deleteStudent">Delete Student entry</button>
        
    </div>
</template>

<script>
export default {
    data() {
        return {
            msg :"This is reference type variable example"
        }
    },
    props : {
        studentlist : Array
    },
    methods : {
        deleteStudent() {
            this.studentlist.pop()
        }
    }
}
</script>