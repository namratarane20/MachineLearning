<template>

   
<div class="container-fluid">
    <Header/>
                         
	<div class="d-flex justify-content-center h-100 col-xl-6">
		<div class="card ">
			<div class="card-header">
				<h3>Sign In</h3>
				
				
			</div>
			<div class="card-body">
				<form>
					<br>
					<div class="input-group form-group">
						<div class="input-group-prepend">
							<br>
							<span class="input-group-text">
								<font-awesome-icon icon="user-secret">
									</font-awesome-icon>
							</span>
						</div>
						<br>
						<input type="text" class="form-control" placeholder="username">
						
					</div>
					<!-- <div class="input-group form-group">
						<div class="input-group-prepend">
							<span class="input-group-text"><i class="fas fa-key"></i></span>
						</div>
						<input type="password" class="form-control" placeholder="password">
					</div> -->
					<br>
					<div class="form-group">
						<input type="submit" value="Login" class="btn float-center login_btn">
					</div>
				</form>
			</div>
			<div class="card-footer">
				<div class="d-flex justify-content-center links">
					Don't have an account?<a href="#">Sign Up</a>
				</div>
				<div class="d-flex justify-content-center">
					<a href="#">Forgot your password?</a>
				</div>
			</div>
		</div>
	</div>
    <Footer/>
</div>

   


    
</template>
<script>
export default {
    
}
</script>
<style scoped>

html,body{
background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ9Ec6XwCsmZaYnLBGP70_tp2VPFU1XO-H_XmbM8D7VVIDdCDdU");
background-size: cover;
background-repeat: no-repeat;
height: 100%;
font-family: 'Numans', sans-serif;
}

.container{
height: 100%;
align-content: center;
}

.card{
height: 370px;
margin-top:100px;
margin-bottom: auto;
width: 400px;
background-color: rgba(50,50,50,0.5) !important;
}

.social_icon span{
font-size: 60px;
margin-left: 10px;
color: #FFC312;
}

.social_icon span:hover{
color: white;
cursor: pointer;
}

.card-header h3{
color: white;
}

.social_icon{
position: absolute;
right: 20px;
top: -45px;
}

.input-group-prepend span{
width: 50px;
background-color: #FFC312;
color: black;
border:0 !important;
}

input:focus{
outline: 0 0 0 0  !important;
box-shadow: 0 0 0 0 !important;

}

.remember{
color: white;
}

.remember input
{
width: 20px;
height: 20px;
margin-left: 15px;
margin-right: 5px;
}

.login_btn{
color: black;
background-color: #FFC312;
width: 100px;
}

.login_btn:hover{
color: black;
background-color: white;
}

.links{
color: white;
}

.links a{
margin-left: 4px;
}

</style>