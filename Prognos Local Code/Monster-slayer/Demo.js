new Vue({
    el:"#app",
    data:{
        heroHealth:100,
        monsterHealth:100,
        remainingMonsterHealth:100,
        remainingHeroHealth:100,
        isGameStarted:false
    },
    methods:{
        startGame(){
           this.isGameStarted=true;
        },
        attack(){
            this.monsterHealth -= Math.floor(Math.random() * 15 +1);
            this.heroHealth -= Math.floor(Math.random() *15 +1) ;
            if(this.heroHealth <= 0){
                this.heroHealth=0;
                alert(" Monster Won .. !!");

            }else if(this.monsterHealth <= 0){
                this.monsterHealth=0;
                alert(" Hero Won .. !!");
            }else{
                this.remainingHealthHero();
                this.remainingHealthMonster()
            }
        },
        speAttack(){
            this.monsterHealth -= Math.floor(Math.random() * 25 +1);
            this.heroHealth -= Math.floor(Math.random() *15 +1) ;
            this.remainingHealthHero();
            this.remainingHealthMonster();
            if(this.heroHealth <= 0){
                this.heroHealth=0;
                this.giveUp();
                alert(" Monster Won .. !!");
            }else if(this.monsterHealth <= 0){
                this.monsterHealth=0;
                this.giveUp();
                alert(" Hero Won .. !!");
            }
        },
        heal(){
            if(this.heroHealth < 90){
                this.heroHealth += 10
                this.remainingHealthHero(0)
            }
        },
        giveUp(){
            this.isGameStarted=false;
            this.heroHealth=100;
            this.monsterHealth=100;
            this.remainingHealthHero();
            this.remainingHealthMonster()
            
        },
        remainingHealthHero(){
            this.remainingHeroHealth = this.heroHealth + "%";
            console.log(this.remainingHeroHealth);
        },
        remainingHealthMonster(){
            this.remainingMonsterHealth = this.monsterHealth + "%";
            console.log(this.remainingMonsterHealth);
        }
    }
})