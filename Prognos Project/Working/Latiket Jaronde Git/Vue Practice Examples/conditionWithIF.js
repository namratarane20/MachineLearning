var x = new Vue({
    el:"#app",
    data: {
        show:false
    }
})

new Vue ({
    el : "#app1",
    data : {
        isActive :true
    }, 
    methods : {
        changeActiveness() {
            this.isActive = !this.isActive
        }
    }
})