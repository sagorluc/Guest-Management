// alert("reading form show password js")
function showPassword(){
    var pass = document.getElementById('id_password')
    if(pass.type == "password"){
        pass.type = 'text'

    }else{
        pass.type = 'password'
    }

}