<template>
<div  class="container">
<div class="jumbotron">
    <h1>this is Cards templete</h1>
<div class="row">
    <div class="card" style="width: 18rem;">
       <img class="card-img-top" src="data:image/jpeg;base64,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" alt="Card image cap"> -->
          <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
         <a href="#" class="btn btn-primary">Go somewhere</a>
          </div>
    </div> &nbsp &nbsp
    <div class="card">
         <div class="card-body">
          This is some text within a card body.
    </div>
    <div class="card" style="width: 18rem;">
         <div class="card-body">
               <h5 class="card-title">Card title</h5>
               <h6 class="card-subtitle mb-2 text-muted">Card subtitle</h6>
               <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
               <a href="#" class="card-link">Card link</a>
               <a href="#" class="card-link">Another link</a>
         </div>
        </div> 
    
    </div>&nbsp &nbsp
    <div class="card" style="width: 18rem;">
           <div class="card-header">
             Featured
        </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item">Cras justo odio</li>
              <li class="list-group-item">Dapibus ac facilisis in</li>
              <li class="list-group-item">Vestibulum at eros</li>
           </ul>
       </div>
       <div class="card" style="width: 18rem;">
            <img class="card-img-top" src="https://www.w3schools.com/bootstrap4/img_avatar3.png" alt="Card image cap">
                <div class="card-body">
                    <h5 class="card-title">Card title</h5>
                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">Cras justo odio</li>
                        <li class="list-group-item">Dapibus ac facilisis in</li>
                        <li class="list-group-item">Vestibulum at eros</li>
                    </ul>
                <div class="card-body">
                    <a href="#" class="card-link">Card link</a>
                    <a href="#" class="card-link">Another link</a>
                </div>
       </div>
       <div class="card">
  <div class="card-header">
    Featured
  </div>
  <div class="card-body">
    <h5 class="card-title">Special title treatment</h5>
    <p class="card-text">With supporting text below as a natural lead-in to additional content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
  <p></p>
  <p></p>
                      <div class="progress">
                           <div class="progress-bar progress-bar-striped" role="progressbar" style="width: 10%" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"></div>
                           </div>
                           <div class="progress">
                             <div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: 25%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
                           </div>
                           <div class="progress">
                             <div class="progress-bar progress-bar-striped bg-info" role="progressbar" style="width: 50%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                           </div>
                           <div class="progress">
                             <div class="progress-bar progress-bar-striped bg-warning" role="progressbar" style="width: 75%" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100"></div>
                           </div>
                           <div class="progress">
                             <div class="progress-bar progress-bar-striped bg-danger" role="progressbar" style="width: 100%" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100"></div>
                           </div>
</div>
  
</div>
</div>
</div>
</template>
<script>
export default {
    
}
</script>
<style lscoped>
img{
    height: 250px;
    width: px;
}
</style>