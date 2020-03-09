var vm = new Vue({
    el: "#compProperty",
    data: {
        counter: 0,
        secCounter: 0,
        fname : " ",
        lname : " ",
        m : 0,
        cm : 0,
        a : 0,
        b : 0
    },
    computed : {
        output : function() {
            console.log('output')
            return this.counter > 5 ? 'greater than 5' : 'less than 5'
        },
        getFullName : function() {
            return this.fname + " " + this.lname
        },
        computeUnit : function() {
            if(this.m != 0 ) {
                this.cm = this.m * 100
            } else {
                this.m = this.cm / 100
            }
        }
    },
    methods : {
        result : function() {
            console.log('method')
            return this.counter > 5 ? 'greater than 5' : 'less than 5'
        }
    }
})