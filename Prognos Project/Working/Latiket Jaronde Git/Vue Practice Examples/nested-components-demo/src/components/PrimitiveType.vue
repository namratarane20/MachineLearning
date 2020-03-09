<template>
    <div>
        <h2> {{ msg }} </h2>

        author name : {{ authorname }}

        <button @click="changeName"> Change name </button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            msg : "This is primitive type variable example"
        }
    },
    props : {
        authorname : String
    },
    methods : {
        changeName() {
            this.authorname = "joker"
        }
    }
}
</script>