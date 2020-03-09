import axios from 'axios'

export default {
fetchNotes(method, params, data){
if (method === 'post'){
return ajax('api/notes/', method, {data})
}
else{
return ajax('api/notes/','get',{})
}
}
}

function ajax(url, method, options){
if(options !== undefined){
var {params = {}, data = {}} = options
} else {
params= data = {}
}
return new Promise((resolve, reject) => {
axios({
url,
method,
params,
data
}).then(res => {
resolve(res)
}, res =>{
reject(res)
})
})
}
