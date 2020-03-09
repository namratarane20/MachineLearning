new Vue({
    el:"#app",
    data : {
        username : '',
        playerTotalHealth : 100,
        playerRemainingHealth : '100%',
        monsterTotalHealth : 100,
        monsterRemainingHealth : '100%',
        heavyAttackOnMonster : 0,
        show:true
    },
    methods : {
        attack : function () {
            this.playerTotalHealth = this.playerTotalHealth - (Math.floor(Math.random()*10))
            this.playerRemainingHealth = this.playerTotalHealth + '%'
            this.monsterTotalHealth = this.monsterTotalHealth - (Math.floor(Math.random()*10))
            this.monsterRemainingHealth = this.monsterTotalHealth + '%'

            if(this.playerTotalHealth === 0 || this.playerTotalHealth < 0) {
                this.playerRemainingHealth = 0%
                alert("PLAYER DEAD.....MONSTER WINS")
            } else if(this.monsterTotalHealth === 0 || this.monsterTotalHealth < 0) {
                this.monsterRemainingHealth = 0%
                alert("MONSTER DEAD.......PLAYER WINS")
            }
        },

        heavyAttack : function() {
            this.playerTotalHealth = this.playerTotalHealth - (Math.floor(Math.random()*10))
            this.playerRemainingHealth = this.playerTotalHealth + '%'

            this.heavyAttackOnMonster = Math.floor(Math.random()*100)
            if(this.heavyAttackOnMonster > 20 && this.heavyAttackOnMonster < 40) {
                this.heavyAttackOnMonster = Math.floor(this.heavyAttackOnMonster/2)
            } else if(this.heavyAttackOnMonster > 40 && this.heavyAttackOnMonster < 60) {
                this.heavyAttackOnMonster = Math.floor(this.heavyAttackOnMonster/3)
            } else if(this.heavyAttackOnMonster > 60 && this.heavyAttackOnMonster < 80) {
                this.heavyAttackOnMonster = Math.floor(this.heavyAttackOnMonster/4)
            } else if(this.heavyAttackOnMonster > 80 && this.heavyAttackOnMonster < 100) {
                this.heavyAttackOnMonster = Math.floor(this.heavyAttackOnMonster/5)
            }

            this.monsterTotalHealth = this.monsterTotalHealth - this.heavyAttackOnMonster
            this.monsterRemainingHealth = this.monsterTotalHealth + '%'

            if(this.playerTotalHealth == 0 || this.playerTotalHealth < 0) {
                this.playerRemainingHealth = 0 + '%'
                alert("PLAYER DEAD.....MONSTER WINS")
            } else if(this.monsterTotalHealth === 0 || this.monsterTotalHealth < 0) {
                this.monsterRemainingHealth = 0 + '%'
                alert("MONSTER DEAD.......PLAYER WINS")
            }
        },

        heal : function() {
            this.playerTotalHealth = this.playerTotalHealth + (Math.floor(Math.random()*10))            
            this.monsterTotalHealth = this.monsterTotalHealth + (Math.floor(Math.random()*10))
        
            if(this.playerTotalHealth > 100 && this.monsterTotalHealth > 100) {
                this.playerTotalHealth = 100
                this.playerRemainingHealth = this.playerTotalHealth + '%'
                this.monsterTotalHealth = 100
                this.monsterRemainingHealth = this.monsterTotalHealth + '%'
            } else if(this.playerTotalHealth > 100 || this.monsterTotalHealth > 100) {
                if(this.playerTotalHealth > 100) {
                    this.playerTotalHealth = 100
                    this.playerRemainingHealth = this.playerTotalHealth + '%'
                } else {
                    this.monsterTotalHealth = 100
                    this.monsterRemainingHealth = this.monsterTotalHealth + '%'
                }
            } else {
                this.playerRemainingHealth = this.playerTotalHealth + '%'
                this.monsterRemainingHealth = this.monsterTotalHealth + '%'
            }
        },

        giveUp : function() {
            alert("PLAYER GIVE UP ..... MONSTER WINS")
        },
        changeDivision() {
            if(this.username != '') {
                this.show = !this.show
            }
        }
    }
})